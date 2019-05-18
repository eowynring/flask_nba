from flask import Flask, render_template, request, json, url_for, redirect
import pymysql
import math
app = Flask(__name__)


@app.route("/")
def index_page():
    return render_template("index.html")


@app.route("/nbanews")
def nbanews():
    datas = page(1) 
    page_all = (getnewsdatas()//20+1)
    # print(datas["datas"])
    return render_template("news.html", list_page_number=datas["list_pagenumber"], page_count_all=page_all, div_datas=datas["datas"])


@app.route("/nbaTeams") 
def nbaTeams():
    return render_template("nbaTeams.html")


def getnewsdatas():
    cur = connect_mysql()
    Sql_count = "select count(*) from newsnba"
    cur.execute(Sql_count)
    count = int(cur.fetchall()[0][0])
    return count


def page(number):
    dict1 = {}
    cur = connect_mysql()
    list_pagenumber = range(number, number+5)
    init_num = number
    Sql_page = "select newsId,newsTitle,newsTimeNow,fromSide from newsnba where newsId >='" + \
        str((init_num-1)*20+1)+"' and newsId < '"+str((init_num-1)*20+21)+"'"
    cur.execute(Sql_page)
    datas_list = cur.fetchall()
    dict1["datas"] = datas_list
    dict1["list_pagenumber"] = list_pagenumber
    return dict1


def details_page(newsid):
    dict1 = {}
    cur = connect_mysql()
    Sql_page = "select newsTitle,detialTime,detailImg,detialCon,detailConImg,detailEditor from newsnba where newsId = '" + \
        str(newsid)+"'"
    cur.execute(Sql_page)
    datas_list = cur.fetchall()
    dict1["details_page"] = datas_list
    return dict1


def connect_mysql():
    connection = pymysql.connect(host="localhost", user="root", passwd="root", db="hupunba", port=3306,
                                 charset='utf8')
    cur = connection.cursor()
    return cur


@app.route("/next_num/<int:page_num>")
def next_num(page_num):
    datas = page(page_num)
    page_all = (getnewsdatas() // 20 + 1)
    # print(datas["datas"])
    return render_template("news.html", div_datas=datas["datas"], list_page_number=datas["list_pagenumber"], page_count_all=page_all)


@app.route("/detail/<int:newsid>")
def detail(newsid):
    datas = details_page(newsid)
    return render_template("detial.html", detail_datas=datas["details_page"][0])


@app.route("/NBATeam/<string:teamName>")
def NBATeam(teamName):
    datas = teamPlayers(teamName)
    print(datas["players"])
    return render_template("players.html", playerList=datas["players"])


def teamPlayers(name):
    dict1 = {}
    cur = connect_mysql()
    Sql_page = "select playerId,playerName,playerImg from players where playerTeam = '"+name+"'"
    cur.execute(Sql_page)
    datas_list = cur.fetchall()
    dict1["players"] = datas_list
    return dict1


@app.route("/NBATeam/NBAplayersInfo/<string:numId>")
def NBAplayersInfo(numId):
    datas = nbaPlayersInfo(numId)
    print(datas["playersInfo"])
    return render_template("playersInfo.html",playerInfoList = datas["playersInfo"] )




def nbaPlayersInfo(numId):
    dict1={}
    cur = connect_mysql()
    sql_select = " select playerName,playerTeam,playerNum,nation,playerImg,high,weight,position,birthday,player_show,nowcontract,detailContract,contract from players where playerId='"+numId+"'"
    cur.execute(sql_select)
    datas_list = cur.fetchall()
    dict1["playersInfo"]=datas_list
    return dict1
    




if __name__ == "__main__":
    app.run(debug=True)
