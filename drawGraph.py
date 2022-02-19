from tkinter.tix import IMAGE
from unicodedata import name
import plotly.graph_objects as go
import plotly.express as px
from PIL import Image
from allAbilities import OtherAbility

class makeGraph():
    def psCompare(dmgP,dmgS, abilityOrder, bar):
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
            name = "Primary target",
            x = x,
            y = yP
            ),
            go.Bar(
            name = "Secondary targets",
            x = x,
            y = yS
            )
        ])
        fig.update_layout(bargap=0)
        fig.update_xaxes(title_text='Tick and Used Abilities', title_font = {"size": 20})
        fig.update_yaxes(title_text='Damage on Primary & Secondary targets', title_font = {"size": 20})

        for tc in range(len(abilityOrder)): #abilities used in order
            if (len(abilityOrder[tc])==0):
                continue
            if(abilityOrder[tc][0].name == "Poison"):
                continue
            if (tc >= 1):
                if (len(abilityOrder[tc-1])!=0):
                    if (abilityOrder[tc][0] == abilityOrder[tc - 1][0]):
                        continue
            source = Image.open(abilityOrder[tc][0].icon)
            fig.add_layout_image(
                source=source,
                xref="x",
                yref="paper",
                x=tc,
                y=0,
                xanchor="center",
                yanchor="top",
                sizex=1,
                sizey=1
            )
        #action bar background
        source = Image.open("./ability_icons/background.png")
        fig.add_layout_image(
            source=source,
            xref="paper",
            yref="paper",
            x=0.19,
            y=1.11,
            xanchor="left",
            yanchor="top",
            sizex=0.68,
            sizey=0.68
        )
        for i in range(len(bar)): #abilities in action bar
            source = Image.open(bar[i].icon)
            fig.add_layout_image(
                source=source,
                xref="paper",
                yref="paper",
                x=0.1987 + i*0.048,
                y=1.091,
                xanchor="left",
                yanchor="top",
                sizex=0.079,
                sizey=0.079
            )
        fig.show()

    def pDetail(dmgP, abilityOrder, bar,otherAbList):
        x = list(range(len(dmgP)))
        abilityDmgData = {}
        barAndOtherAb = bar + otherAbList
        for ability in barAndOtherAb:
            abilityDmgData[ability] = []
            for hitsInTickDict in dmgP:
                if (ability in hitsInTickDict):
                    abilityDmgData[ability].append(sum(hitsInTickDict[ability]))
                else:
                    abilityDmgData[ability].append(0)
            if(sum(abilityDmgData[ability]) == 0):
                del abilityDmgData[ability]
        abilityDmgDataName = {}
        for index in abilityDmgData: #fill similar data list but with ability name as index
            abilityDmgDataName[index.name] = abilityDmgData[index]
        abilityDmgDataAll = []
        for index in abilityDmgDataName:
            abilityDmgDataAll.append(go.Bar(name=index, x=x, y=abilityDmgDataName[index]))
        fig = go.Figure(data=abilityDmgDataAll)
        fig.update_layout(barmode="stack", bargap=0)
        fig.update_xaxes(title_text='Tick and Used Abilities', title_font = {"size": 20})
        fig.update_yaxes(title_text='Damage on Primary target', title_font = {"size": 20})

        #from below, same as other 2
        for tc in range(len(abilityOrder)): #abilities used in order
            if (len(abilityOrder[tc])==0):
                continue
            if(abilityOrder[tc][0].name == "Poison"):
                continue
            if (tc >= 1):
                if (len(abilityOrder[tc-1])!=0):
                    if (abilityOrder[tc][0] == abilityOrder[tc - 1][0]):
                        continue
            source = Image.open(abilityOrder[tc][0].icon)
            fig.add_layout_image(
                source=source,
                xref="x",
                yref="paper",
                x=tc,
                y=0,
                xanchor="center",
                yanchor="top",
                sizex=1,
                sizey=1
            )
        
        #action bar background
        source = Image.open("./ability_icons/background.png")
        fig.add_layout_image(
            source=source,
            xref="paper",
            yref="paper",
            x=0.19,
            y=1.11,
            xanchor="left",
            yanchor="top",
            sizex=0.68,
            sizey=0.68
        )
        for i in range(len(bar)): #abilities in action bar
            source = Image.open(bar[i].icon)
            fig.add_layout_image(
                source=source,
                xref="paper",
                yref="paper",
                x=0.1987 + i*0.048,
                y=1.091,
                xanchor="left",
                yanchor="top",
                sizex=0.079,
                sizey=0.079
            )
        fig.show()


    def sDetail(dmgS, abilityOrder, bar, otherAbList):
        x = list(range(len(dmgS)))
        abilityDmgData = {}
        barAndOtherAb = bar + otherAbList
        for ability in barAndOtherAb:
            abilityDmgData[ability] = []
            for hitsInTickDict in dmgS:
                if (ability in hitsInTickDict):
                    abilityDmgData[ability].append(sum(hitsInTickDict[ability]))
                else:
                    abilityDmgData[ability].append(0)
            if(sum(abilityDmgData[ability]) == 0):
                del abilityDmgData[ability]
        abilityDmgDataName = {}
        for index in abilityDmgData: #fill similar data list but with ability name as index
            abilityDmgDataName[index.name] = abilityDmgData[index]
        abilityDmgDataAll = []
        for index in abilityDmgDataName:
            abilityDmgDataAll.append(go.Bar(name=index, x=x, y=abilityDmgDataName[index]))
        fig = go.Figure(data=abilityDmgDataAll)


        """x = list(range(len(dmgS)))
        abilityDmgData = {}
        barAndOtherAb = bar + otherAbList
        for ability in barAndOtherAb:
            abilityDmgData[ability.name] = []
            for hitsInTickDict in dmgS:
                if (ability in hitsInTickDict):
                    abilityDmgData[ability.name].append(sum(hitsInTickDict[ability]))
                else:
                    abilityDmgData[ability.name].append(0)
            if(sum(abilityDmgData[ability.name]) == 0):
                del abilityDmgData[ability.name]
        abilityDmgDataAll = []
        for index in abilityDmgData:
            abilityDmgDataAll.append(go.Bar(name=index, x=x, y=abilityDmgData[index]))
        fig = go.Figure(data=abilityDmgDataAll)"""
        fig.update_layout(barmode="stack", bargap=0)
        fig.update_xaxes(title_text='Tick and Used Abilities', title_font = {"size": 20})
        fig.update_yaxes(title_text='Average damage on Secondary targets', title_font = {"size": 20})

        #from below, same as other 2
        for tc in range(len(abilityOrder)): #abilities used in order
            if (len(abilityOrder[tc])==0):
                continue
            if(abilityOrder[tc][0].name == "Poison"):
                continue
            if (tc >= 1):
                if (len(abilityOrder[tc-1])!=0):
                    if (abilityOrder[tc][0] == abilityOrder[tc - 1][0]):
                        continue
            source = Image.open(abilityOrder[tc][0].icon)
            fig.add_layout_image(
                source=source,
                xref="x",
                yref="paper",
                x=tc,
                y=0,
                xanchor="center",
                yanchor="top",
                sizex=1,
                sizey=1
            )
        #action bar background
        source = Image.open("./ability_icons/background.png")
        fig.add_layout_image(
            source=source,
            xref="paper",
            yref="paper",
            x=0.19,
            y=1.11,
            xanchor="left",
            yanchor="top",
            sizex=0.68,
            sizey=0.68
        )
        for i in range(len(bar)): #abilities in action bar
            source = Image.open(bar[i].icon)
            fig.add_layout_image(
                source=source,
                xref="paper",
                yref="paper",
                x=0.1987 + i*0.048,
                y=1.091,
                xanchor="left",
                yanchor="top",
                sizex=0.079,
                sizey=0.079
            )
        fig.show()