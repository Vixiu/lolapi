from Lcu import LcuRequest

lcu = LcuRequest()
# /network-testing/v1/experiments
# /riotclient/kill-and-restart-ux
# /network-testing/v1/game-latency
print(lcu.getdata("/plugin-manager/v2/descriptions").text)
