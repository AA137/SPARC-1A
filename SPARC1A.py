#sim(n) explanation:
#prices: list of prices for each week. meandic: dictionary that links each gas station with a "mean value" for how much higher/lower its prices are than the "average" price of gas for that week
#quotedic: stores prices that each gas station quotes each week. emadic: stores an estimate for each week's price using prices of weeks around it. diffdic: tracks how much higher/lower each quote is from the "average" price of gas that week
#cost: tracks amount spent on gas. idealcost: tracks amount spent if you had gone to the cheapest gas station each time.
#weekno: week number. minmean: cheapest gas station.
#normal(n, sd) explanation:
#Uses Central Limit Theorem to get an approximately normal distribution. Uses fact that standard deviation of a uniform distribution is n*sqrt(1/12) where n is the width of the distribution.
#testsim(k,n) explanation:
#perc: running counter of percent over the ideal cost

import random
import math
def sim(n):
	prices=[]
	meandic={str(i):normal(30,0.05) for i in range(n)}
	quotedic={}
	emadic={}
	diffdic={str(i):0 for i in range(n)}
	cost=0
	idealcost=0
	weekno=0
	clone=meandic
	key_min = min(meandic.keys(), key=(lambda k: meandic[k]))
	minmean=meandic[key_min]
	for i in range(1001):
		if len(prices)==0:
			prices.append(2.5)
		else:
				prices.append(round(prices[i-1]+normal(30,0.025),4))
	while len(clone)!=1:
				for i in range(4):
					for p in clone:
						quotedic.update({p:(round(prices[weekno]+meandic[p]+normal(30,0.015),4), weekno)})
						idealcost+=(prices[weekno]+minmean+normal(30,0.015))
						cost+=quotedic[p][0]
						weekno+=1
				for p in clone:
					numerator=0
					denominator=0
					for j in clone:
						numerator+=round(quotedic[j][0]/((1.6)**(abs(quotedic[p][1]-quotedic[j][1]))),4)
						denominator+=round((1/((1.6)**(abs(quotedic[p][1]-quotedic[j][1])))),4)
					emadic.update({p:round(numerator/denominator, 4)})
					diffdic.update({str(p):round((diffdic[p]-emadic[p]+quotedic[p][0]),4)})
				sortedrankings = sorted(diffdic.items(), key=lambda kv: kv[1])
				clone=dict(sortedrankings[:-(-len(sortedrankings)//2)])
				diffdic={i:diffdic[i] for i in diffdic if i in clone}
				quotedic={}
				emadic={}
	while weekno<1001:
		cost+=round(prices[weekno]+meandic[list(clone.keys())[0]]+normal(30,0.015),4)
		idealcost+=prices[weekno]+minmean+normal(30,0.015)
		weekno+=1
	return 100*(cost/idealcost)-100


def normal(n, sd):
    counter = 0
    for i in range(n):
        counter += random.uniform(-1, 1)
    return (counter * math.sqrt(3 * n) * sd) / n

#sim(20)
def testsim(k,n):
	perc=0
	for i in range(k):
		perc+=sim(n)
	print("On average, you spent "+str(perc/k)+" percent more than you would've if you went to the cheapest gas station every time")

testsim(30,12)