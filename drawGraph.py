from tkinter.tix import IMAGE
from unicodedata import name
import plotly.graph_objects as go
from PIL import Image
from allAbilities import OtherAbility

class makeGraph():
    def psCompare(dmgP,dmgS, abilityOrder, bar):
        x = list(range(len(dmgP)))
        yP, yS = [], []
        for hitsInTick in dmgP:
            dmgInTick = 0
            for abiIndex in hitsInTick:
                dmgInTick += hitsInTick[abiIndex]
            yP.append(dmgInTick)
        for hitsInTick in dmgS:
            dmgInTick = 0
            for abiIndex in hitsInTick:
                dmgInTick += hitsInTick[abiIndex]
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

        for tc, ability in enumerate(abilityOrder): #add used abilities under x axis
            if type(ability) == OtherAbility:
                continue
            if tc >= 1:
                if type(abilityOrder[tc-1]) != OtherAbility:
                    if ability == abilityOrder[tc - 1]:
                        continue
            source = Image.open(ability.icon)
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

    def pDetail(dmgP, abilityOrder, bar, otherAbList, dps):
        x = list(range(len(dmgP)))
        barAndOtherAb = bar + otherAbList
        abilityData = []
        for ability in barAndOtherAb:
            abdmg = []
            sum = 0
            for dictTick in dmgP:
                if ability.name in dictTick:
                    sum += dictTick[ability.name]
                    abdmg.append(dictTick[ability.name])
                else:
                    abdmg.append(0)
            if sum:
                abilityData.append(go.Bar(name=ability.name, x=x, y=abdmg))

        fig = go.Figure(data=abilityData)
        fig.update_layout(barmode="stack", bargap=0)
        fig.update_xaxes(title_text='Tick and Used Abilities (Primary target) ('+str(dps)+' dps)', title_font = {"size": 20})
        fig.update_yaxes(title_text='Damage on Primary target', title_font = {"size": 20})

        #from below, same as other 2
        for tc, ability in enumerate(abilityOrder): #add used abilities under x axis
            if type(ability) == OtherAbility:
                continue
            if tc >= 1:
                if type(abilityOrder[tc-1]) != OtherAbility:
                    if ability == abilityOrder[tc - 1]:
                        continue
            source = Image.open(ability.icon)
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


    def sDetail(dmgS, abilityOrder, bar, otherAbList, dps):
        x = list(range(len(dmgS)))
        barAndOtherAb = bar + otherAbList
        abilityData = []
        for ability in barAndOtherAb:
            abdmg = []
            sum = 0
            for dictTick in dmgS:
                if ability.name in dictTick:
                    sum += dictTick[ability.name]
                    abdmg.append(dictTick[ability.name])
                else:
                    abdmg.append(0)
            if sum:
                abilityData.append(go.Bar(name=ability.name, x=x, y=abdmg))

        fig = go.Figure(data=abilityData)
        fig.update_layout(barmode="stack", bargap=0)
        fig.update_xaxes(title_text='Tick and Used Abilities (Secondary targets\'average) ('+str(dps)+' dps)', title_font = {"size": 20})
        fig.update_yaxes(title_text='Average damage on Secondary targets', title_font = {"size": 20})

        #from below, same as other 2
        for tc, ability in enumerate(abilityOrder): #add used abilities under x axis
            if type(ability) == OtherAbility:
                continue
            if tc >= 1:
                if type(abilityOrder[tc-1]) != OtherAbility:
                    if ability == abilityOrder[tc - 1]:
                        continue
            source = Image.open(ability.icon)
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