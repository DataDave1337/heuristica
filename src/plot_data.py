import seaborn as sns
import pandas as pd
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

    def assign_result(self, rules):
        df = self.data

        df['rule_flag'] = 0
        # rule application
        for rule_dict in rules:
            df.loc[df[rule_dict['rule_attr']].between(rule_dict['attr_min'], rule_dict['attr_max'], inclusive=True), 'rule_flag'] = 1

        df.loc[(df['rule_flag'] == 0) & (df['bin_target'] == 0), 'result'] = 'True Negatives'
        df.loc[(df['rule_flag'] == 1) & (df['bin_target'] == 0), 'result'] = 'Falsely covered'
        df.loc[(df['rule_flag'] == 0) & (df['bin_target'] == 1), 'result'] = 'Not covered'
        df.loc[(df['rule_flag'] == 1) & (df['bin_target'] == 1), 'result'] = 'Rightly covered'

    def fill_ranges(self, rules):
        for rule_dict in rules:
            rule_attr = rule_dict['rule_attr']
            
            # assign rule results
            if rule_dict['attr_min'] is None:
                rule_dict['attr_min'] = self.data[rule_attr].min()

            if rule_dict['attr_max'] is None:
                rule_dict['attr_max'] = self.data[rule_attr].max()

        return rules

    def scatter_rule(self, scatter_cols, rules, ax=None):
        df = self.data

        rules = self.fill_ranges(rules)
        # assign rule results        
        self.assign_result(rules)
        
        # scatter plot rule results
        col_col = 'result'
        cmap = create_colormap()
        
        # pandas version
        c = [cmap[r] for r in df[col_col]]
        # if ax is None:
        #     axes = pd.plotting.scatter_matrix(df[scatter_cols+[col_col]], c=c, s=100, alpha=0.7)
        #     fig = axes[0][0].get_figure()
        # else:
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
            col_idx = scatter_cols.index(rule_attr)
            col_axes = axes[:, col_idx]
            row_axes = axes[col_idx, :]
            if col_idx != -1:
                for ax in col_axes:
                    ax.axvspan(attr_min, attr_max, alpha=0.2, color='C1')
                for i, ax in enumerate(row_axes):
                    if i != col_idx:
                        ax.axhspan(attr_min, attr_max, alpha=0.2, color='C1')
        # calc rule stats
        # self.print_additional_stats()
        plt.tight_layout()
        
    def calc_additional_stats(self):
        conf_mat = pd.crosstab(self.data['bin_target'], self.data['rule_flag'])
        
        print(conf_mat)
        tp = conf_mat.iloc[1, 1]
        tn = conf_mat.iloc[0, 0]
        fp = conf_mat.iloc[1, 0]
        fn = conf_mat.iloc[0, 1]
        result_counts = self.data['result'].value_counts()

        confidence = tp / (fp + tp)
        support = self.data['rule_flag'].sum()/len(self.data)
        target_rate = self.data['bin_target'].sum()/len(self.data)
        lift = confidence / target_rate
        recall = tp / (fn + tp)
        print(f'''
        Rule confidence: {confidence: 0.3f}
        Support:         {support: 0.3f}
        Lift:            {lift: 0.3f}
        Recall:          {recall:0.3f}
        -----------------------------''')
        print(conf_mat, self.data['result'].value_counts())