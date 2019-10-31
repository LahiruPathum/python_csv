import mysql.connector
from mysql.connector import Error
import csv

event_id=8

def getdata():
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='isacaAdmin',
                                             user='root',
                                             password='root')

        sql_select_Query_team = "SELECT T.id,T.teamName,T.proposal,I.instituteName FROM ihack_teams T, institutes I WHERE T.instituteId=I.id AND T.event_id=8"
        cursor = connection.cursor()
        cursor.execute(sql_select_Query_team)
        team_records = cursor.fetchall()

        data=[]
        for trow in team_records:
            sql_select_Query_participants = "SELECT firstName,lastName,contact,yearOfStudy,meal,tShirtSize FROM ihack_participants WHERE team_id = "+str(trow[0])+" AND event_id ="+str(event_id)
            cursor.execute(sql_select_Query_participants)
            participant_records = cursor.fetchall()
            
            team_data={'id':trow[0],'teamName':trow[1],'proposal':trow[2],'instituteName':trow[3]}
            i = 1
            for prow in participant_records:
                team_data['name_'+str(i)]=prow[0]+" "+prow[1]
                team_data['contact_'+str(i)]=prow[2]
                team_data['yearOfStudy_'+str(i)]=prow[3]
                team_data['meal_'+str(i)]=prow[4]
                team_data['tshirtSize_'+str(i)]=prow[5]
                i=i+1
            data.append(team_data)  
        print(data)
        return data

    except Error as e:
        print("Error reading data from MySQL table", e)
    finally:
        if (connection.is_connected()):
            connection.close()
            cursor.close()
            print("MySQL connection is closed")

def writedata():
    with open('isaca.csv', 'w') as csvfile:
        data = getdata()
        fields = ['id', 'teamName','proposal','instituteName','name_1','contact_1','yearOfStudy_1','meal_1','tshirtSize_1','name_2','contact_2','yearOfStudy_2','meal_2','tshirtSize_2',
                  'name_3','contact_3','yearOfStudy_3','meal_3','tshirtSize_3','name_4','contact_4','yearOfStudy_4','meal_4','tshirtSize_4',]
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writeheader()
        writer.writerows(data)

    print("file writing complete.")

writedata()
#SELECT T.id,T.teamName,T.proposal,I.instituteName FROM ihack_teams T, institutes I WHERE T.instituteId=I.id AND T.event_id=8
#SELECT firstName,lastName,contact,yearOfStudy,meal,tShirtSize FROM ihack_participants WHERE team_id =  AND event_id = 
