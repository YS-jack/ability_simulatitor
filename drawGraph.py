import plotly.graph_objects as go
import plotly.express as px

class makeGraph():
    def psCompare(dmgP,dmgS):
        x = list(range(len(dmgP)))
        yP = []
        for hitsInTick in dmgP:
            dmgInTick = 0
            for abiIndex in hitsInTick:
                dmgInTick += sum(hitsInTick[abiIndex])
            yP.append(dmgInTick)
        yS = []
        for hitsInTick in dmgS:
            dmgInTick = 0
            for abiIndex in hitsInTick:
                dmgInTick += sum(hitsInTick[abiIndex])
            yS.append(dmgInTick)
        
        fig = go.Figure(data=[go.Bar(
            name = "Damage to primary target",
            x = x,
            y = yP
            ),
            go.Bar(
            name = "Damage to secondary targets",
            x = x,
            y = yS
            )
        ])
        fig.update_layout(bargap=0)
        fig.show()

    def pDetail(dmgP):
        pass

    def sDetail(dmgS):
        pass