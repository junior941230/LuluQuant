from backend import Backtest
backtest = Backtest()
stockId = "3481"
startStr = "2006-10-24"
endStr = "2026-03-06"
inputFund = 500000
resultObj = backtest.runSimulation(stockId, startStr, endStr, inputFund)
rawDf = backtest.processResult()
#pyside6-uic  .\UI\UImainWindow.ui -o .\UI\UImainWindow.py