import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def create_colormap():
    cmap = sns.color_palette("Paired")

    # scatter plot rule results
    col_col = 'result'
    cmap = {
        'True Negatives': cmap[0],
        'Falsely covered': cmap[1],
        'Not covered': cmap[2],
        'Rightly covered': cmap[3]
    }

    #     cmap = {
    #         'True Negatives': 'C0',
    #         'Falsely covered': 'C3',
    #         'Not covered': 'C4',
    #         'Rightly covered': 'C2'
    #     }

    return cmap

class ScatterPlotter():

    def __init__(self, data):
        # self.figure
        self.data = data
        self.stats = pd.DataFrame(columns=['rule_id', 'confidence', 'support',
                                           'lift', 'recall',
                                           'tp', 'tn', 'fp', 'fn'])

    def get_stats(self, y_true, y_pred, rule_id):
        # calc stats
        conf_mat = pd.crosstab(y_true, y_pred)
        tp = conf_mat.iloc[1, 1]
        tn = conf_mat.iloc[0, 0]
        fp = conf_mat.iloc[0, 1]
        fn = conf_mat.iloc[1, 0]

        confidence = tp / (fp + tp)
        support = y_pred.sum()/len(y_true)
        target_rate = y_true.sum()/len(y_true)
        lift = confidence / target_rate
        recall = tp / (fn + tp)
        # TODO: WRAcc Score
        result_dict = {
            'rule_id': rule_id,
            'confidence': confidence,
            'support': support,
            'lift': lift,
            'recall': recall,
            'tp': tp,
            'tn': tn,
            'fp': fp,
            'fn': fn
        }
        return result_dict

    def assign_result(self, rules):
        df = self.data

        stats = []
        total_rule_flag = np.zeros(len(df))
        header = ['rule_id','confidence','support', 'lift', 'recall', 'tp', 'tn', 'fp', 'fn']

        for rule_dict in rules:
            rule_id = rule_dict['rule_id']
            attr = rule_dict['rule_attr']
            min_val = rule_dict['attr_min']
            max_val = rule_dict['attr_max']

            single_rule_flag = np.zeros(len(df))
            rule_bool_arr = df[attr].between(min_val, max_val, inclusive=True)
            single_rule_flag[rule_bool_arr] = 1
            total_rule_flag[rule_bool_arr] = 1
            stat = self.get_stats(df['bin_target'], single_rule_flag, rule_id)
            stats.append(stat)

        df['rule_flag'] = total_rule_flag
        df.loc[(df['rule_flag'] == 0) & (df['bin_target'] == 0), 'result'] = 'True Negatives'
        df.loc[(df['rule_flag'] == 1) & (df['bin_target'] == 0), 'result'] = 'Falsely covered'
        df.loc[(df['rule_flag'] == 0) & (df['bin_target'] == 1), 'result'] = 'Not covered'
        df.loc[(df['rule_flag'] == 1) & (df['bin_target'] == 1), 'result'] = 'Rightly covered'

        if rules:
            stats.append(self.get_stats(df['bin_target'], total_rule_flag, 'Total Ruleset'))
            stats_df = pd.DataFrame(stats)
            stats_df = stats_df.round(decimals=3)
            self.stats = stats_df[header]
        else:
            self.stats = pd.DataFrame(columns=header)

    def fill_ranges(self, rules):
        for rule_dict in rules:
            rule_attr = rule_dict['rule_attr']
            
            # assign rule results
            if rule_dict['attr_min'] is None:
                rule_dict['attr_min'] = self.data[rule_attr].min()

            if rule_dict['attr_max'] is None:
                rule_dict['attr_max'] = self.data[rule_attr].max()

        return rules

    def get_rule_stats(self):
        return self.stats

    def scatter_rule(self, scatter_cols, rules, ax):
        df = self.data

        rules = self.fill_ranges(rules)
        # assign rule results        
        self.assign_result(rules)
        
        # scatter plot rule results
        col_col = 'result'
        cmap = create_colormap()
        
        # pandas version
        c = [cmap[r] for r in df[col_col]]
        axes = pd.plotting.scatter_matrix(df[scatter_cols+[col_col]], c=c, s=100, alpha=0.7, ax=ax)
        # seaborn version
        # pair_plot = sns.pairplot(df[scatter_cols+[col_col]],
        #                         hue=col_col,
        #                         palette=cmap,
        #                         diag_kind='hist',
        #                         diag_kws={'alpha': 0.7},
        #                         ax=ax)
        # plot rule coverage
        for rule_dict in rules:
            rule_attr = rule_dict['rule_attr']
            attr_min = rule_dict['attr_min']
            attr_max = rule_dict['attr_max']
            
            if rule_attr in scatter_cols:
                col_idx = scatter_cols.index(rule_attr)
                col_axes = axes[:, col_idx]
                row_axes = axes[col_idx, :]
                if col_idx != -1:
                    for ax in col_axes:
                        ax.axvspan(attr_min, attr_max, alpha=0.2, color='C1')
                    for i, ax in enumerate(row_axes):
                        if i != col_idx:
                            ax.axhspan(attr_min, attr_max, alpha=0.2, color='C1')

        plt.tight_layout()
