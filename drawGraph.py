import plotly.express as px

class makeGraph():
    def psCompare(dmgP,dmgS):
        df = px.data.tips()
        fig = px.histogram(df, x="sex", y="total_bill",
             color='smoker', barmode='group',
             histfunc='avg',
             height=400)
        print(fig.to_dict())
        fig.show()
        

    def pDetail(dmgP):
        pass

    def sDetail(dmgS):
        pass