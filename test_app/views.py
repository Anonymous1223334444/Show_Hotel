from django.shortcuts import render
from test_app import forms
from django.db import connection
import pymysql


def index1(request):
    spectacle_id=None
    spectacle_name=None
    spectacle_date=None
    spectacle_categorie=None
    request_1 = None
    result = None
    error_message = None
    spectacle_name=None

    # DateField from django form
    form = forms.DateForm()
    # Select Data from mysql database 
    with connection.cursor() as cursor:
        cursor.execute("SELECT id FROM spectacle ORDER BY id DESC")
        all_spectacle = cursor.fetchall()

    context = {'form': form, 'all_spectacle': all_spectacle}
    # The action to perform when submiting the form
    if request.method == 'POST':
        if 'action' in request.POST:
            action = request.POST['action']
            if action == 'btn_1':
                sql_syntax = request.POST.get('sql_syntax', '')
                try:
                    result = execute_sql(sql_syntax)
                except pymysql.Error as e:
                    error_message = str(e)
                context['result'] = result
            elif action == 'btn_2':
                # spectacle
                spectacle_id = request.POST.get('spectacle_id')
                
                with connection.cursor() as cursor:        
                    cursor.execute(f"SELECT name FROM spectacle WHERE id={spectacle_id}")
                    spectacle_name = cursor.fetchone()[0]
                with connection.cursor() as cursor:        
                    cursor.execute(f"SELECT date_spectacle FROM spectacle WHERE id={spectacle_id}")
                    spectacle_date = cursor.fetchone()[0]
                with connection.cursor() as cursor:        
                    cursor.execute(f"SELECT categorie_spectacle FROM spectacle WHERE id={spectacle_id}")
                    spectacle_categorie = cursor.fetchone()[0]
                with connection.cursor() as cursor:        
                    cursor.execute(f"""
                    SELECT pos.spectacle, pos.hotel, CONCAT_WS(' ', pos.Distance, 'm') FROM 
                    (SELECT h.id AS hotel, s.id as spectacle, s.date_spectacle,
	                    CASE
                            WHEN s.ville_id = h.ville_id THEN
                                ROUND(SQRT(POWER(s.loc_X - h.loc_X, 2) + POWER(s.loc_Y - h.loc_Y, 2)), 1)
                            ELSE 
                                ROUND(SQRT(POWER(h.loc_X, 2) + POWER(h.loc_Y, 2)) + SQRT(POWER(s.loc_X, 2) + POWER(s.loc_Y, 2)) + d.dist, 1)
                        END AS "Distance"
                    FROM distance d 
                    JOIN ville v1 ON d.id_ville1=v1.id
                    JOIN ville v2 ON d.id_ville2=v2.id
                    JOIN hotel h ON v1.id=h.ville_id OR v2.id=h.ville_id
                    JOIN spectacle s ON v1.id=s.ville_id OR v2.id=s.ville_id 
                    GROUP BY h.id, s.id, Distance order by h.id, s.id) AS pos 
                    WHERE pos.Distance<5000 AND pos.spectacle={spectacle_id}
                    GROUP BY pos.spectacle, pos.hotel, pos.Distance ORDER BY pos.Distance;
                """)

                    request_1 = cursor.fetchall()
                
                context['spectacle_id'] = spectacle_id
                context['spectacle_name'] = spectacle_name
                context['spectacle_date'] = spectacle_date
                context['spectacle_categorie'] = spectacle_categorie
                context['request_1'] = request_1

    return render(request, 'index1.html', context)


def index2(request):
    ville_id=None
    ville_name=None
    request_2 = None
    result = None
    error_message = None
    form = forms.DateForm(request.POST)
    # selected_date = forms.DateForm(request.POST)
    
    # Select Data from mysql database 
    with connection.cursor() as cursor:
        cursor.execute("SELECT id FROM ville ORDER BY id DESC")
        all_ville = cursor.fetchall()

    context = {'all_ville': all_ville, 'form': form}
    # The action to perform when submiting the form
    if request.method == 'POST':
        if 'action' in request.POST:
            action = request.POST['action']
            if action == 'btn_1':
                sql_syntax = request.POST.get('sql_syntax', '')
                try:
                    result = execute_sql(sql_syntax)
                except pymysql.Error as e:
                    error_message = str(e)
                context['result'] = result
            elif action == 'btn_2':
                # ville
                ville_id = request.POST.get('ville_id')
                # DateField from django form
                if form.is_valid():
                    selected_date = form.cleaned_data['date_field']
                else:
                    form = forms.DateForm()
                with connection.cursor() as cursor:        
                    cursor.execute(f"SELECT nom_ville FROM ville WHERE id={ville_id}")
                    ville_name = cursor.fetchone()[0]
                with connection.cursor() as cursor:        
                    cursor.execute(f"""SELECT id AS id_hotel, nbr_room, h.ville_id,
                                        CASE 
                                            WHEN hr.etat="Oc" 
                                            THEN "Tout occupe" 
                                        END AS etat
                                    FROM (SELECT nbr_room, id, ville_id FROM hotel) AS h
                                    JOIN (SELECT COUNT(*) AS room_dispo, hotel_id, etat FROM hotel_room 
                                    WHERE etat="Oc" GROUP BY hotel_id) AS hr 
                                    ON hr.hotel_id=h.id WHERE h.nbr_room=hr.room_dispo AND h.ville_id={ville_id}""")
                    request_2 = cursor.fetchall()
                context['ville_id'] = ville_id
                context['ville_name'] = ville_name
                context['selected_date'] = selected_date
                context['request_2'] = request_2

    return render(request, 'index2.html', context)

def index3(request):
    ville_id=None
    ville_name=None
    request_3 = None
    result = None
    error_message = None
    form = forms.DateForm(request.POST)
    # selected_date = forms.DateForm(request.POST)
    
    # Select Data from mysql database 
    with connection.cursor() as cursor:
        cursor.execute("SELECT id FROM ville ORDER BY id DESC")
        all_ville = cursor.fetchall()

    context = {'all_ville': all_ville, 'form': form}
    # The action to perform when submiting the form
    if request.method == 'POST':
        if 'action' in request.POST:
            action = request.POST['action']
            if action == 'btn_1':
                sql_syntax = request.POST.get('sql_syntax', '')
                try:
                    result = execute_sql(sql_syntax)
                except pymysql.Error as e:
                    error_message = str(e)
                context['result'] = result
            elif action == 'btn_2':
                # ville
                ville_id = request.POST.get('ville_id')
                # DateField from django form
                if form.is_valid():
                    selected_date = form.cleaned_data['date_field']
                else:
                    form = forms.DateForm()
                with connection.cursor() as cursor:        
                    cursor.execute(f"SELECT nom_ville FROM ville WHERE id={ville_id}")
                    ville_name = cursor.fetchone()[0]
                with connection.cursor() as cursor:        
                    cursor.execute(f"""SELECT tab_p.ville_id As ville_id, tab_p.name AS 'Nom hotel', CONCAT_WS("", MIN(tab_p.prix), " £") AS prix_chambre_moins_cher FROM 
                                        (SELECT h.name, v.nom_ville, v.id AS ville_id, hr.prix, hr.id 
                                        FROM hotel h JOIN ville v ON h.ville_id=v.id
                                        JOIN hotel_room hr ON hr.hotel_id=h.id
                                        WHERE v.id={ville_id} AND hr.categorie='C' AND hr.etat='Li') tab_p GROUP BY tab_p.name, tab_p.ville_id;
                                    """)
                    request_3 = cursor.fetchall()
                context['ville_id'] = ville_id
                context['ville_name'] = ville_name
                context['selected_date'] = selected_date
                context['request_3'] = request_3

    return render(request, 'index3.html', context)

def index4(request):
    request_4 = None
    result = None
    error_message = None
    # selected_date = forms.DateForm(request.POST)
    

    context = {}
    # The action to perform when submiting the form
    if request.method == 'POST':
        if 'action' in request.POST:
            action = request.POST['action']
            if action == 'btn_1':
                sql_syntax = request.POST.get('sql_syntax', '')
                try:
                    result = execute_sql(sql_syntax)
                except pymysql.Error as e:
                    error_message = str(e)
                context['result'] = result
            elif action == 'btn_2':
                with connection.cursor() as cursor:        
                    cursor.execute(f"""SELECT S.id, S.ville, CONCAT_WS(' ', S.prix_sejour_3_jour, '£')
                                        FROM (SELECT v.id, v.nom_ville AS ville, SUM(hr.prix)*2+SUM(ts.prix) AS prix_sejour_3_jour
                                        FROM ville v
                                        JOIN hotel h ON h.ville_id=v.id
                                        JOIN hotel_room hr ON hr.hotel_id=h.id
                                        JOIN reservation r ON r.room_id=hr.id 
                                        JOIN spectacle s ON s.ville_id=v.id
                                        JOIN ticket_spectacle ts ON ts.spectacle_id=s.id WHERE
                                        s.date_spectacle BETWEEN r.date_reservation_debut AND r.date_reservation_fin
                                        GROUP BY v.nom_ville, v.id) AS S
                                        ORDER BY S.prix_sejour_3_jour DESC
                                        LIMIT 1;
                                    """)
                    request_4 = cursor.fetchall()
                context['request_4'] = request_4

    return render(request, 'index4.html', context)

def index5(request):
    request_5 = None
    result = None
    error_message = None
    
    context = {}
    # The action to perform when submiting the form
    if request.method == 'POST':
        if 'action' in request.POST:
            action = request.POST['action']
            if action == 'btn_1':
                sql_syntax = request.POST.get('sql_syntax', '')
                try:
                    result = execute_sql(sql_syntax)
                except pymysql.Error as e:
                    error_message = str(e)
                context['result'] = result
            elif action == 'btn_2':
                with connection.cursor() as cursor:        
                    cursor.execute(f"""SELECT P.id, P.name_client, P.nbr_reserv, CONCAT_WS(' ', P.prix_sejour, '£') AS prix_sejour FROM (SELECT c.id, 
                                        CONCAT_WS(' ', c.prenom, c.nom) AS name_client,
                                        COUNT(r.client_id) AS nbr_reserv, SUM(hr.prix) AS prix_sejour
                                        FROM client c JOIN reservation r ON r.client_id = c.id 
                                        JOIN hotel_room hr ON r.room_id = hr.id
                                        GROUP BY c.id, CONCAT_WS(' ', c.prenom, c.nom)) AS P

                                        JOIN (SELECT r.room_id, r.client_id, hr.prix FROM client c 
                                        JOIN reservation r ON r.client_id = c.id 
                                        JOIN hotel_room hr ON r.room_id = hr.id
                                        GROUP BY r.room_id, r.client_id) AS ch ON ch.client_id = P.id

                                        WHERE P.prix_sejour >=600 AND ch.prix>100
                                        GROUP BY P.id, P.name_client, P.nbr_reserv, P.prix_sejour;
                                    """)
                    request_5 = cursor.fetchall()
                context['request_5'] = request_5

    return render(request, 'index5.html', context)


def extra1(request):
    extra_1 = None
    result = None
    error_message = None
    
    context = {}
    # The action to perform when submiting the form
    if request.method == 'POST':
        if 'action' in request.POST:
            action = request.POST['action']
            if action == 'btn_1':
                sql_syntax = request.POST.get('sql_syntax', '')
                try:
                    result = execute_sql(sql_syntax)
                except pymysql.Error as e:
                    error_message = str(e)
                context['result'] = result
            
    with connection.cursor() as cursor:        
        cursor.execute(f"""SELECT v.id, v.nom_ville, COUNT(*) AS Nbr_hotel FROM ville v
                            JOIN hotel h ON h.ville_id=v.id GROUP BY ville_id ORDER BY Nbr_hotel, v.id;
                        """)
        extra_1 = cursor.fetchall()
    context['extra_1'] = extra_1

    return render(request, 'extra1.html', context)

def extra2(request):
    extra_2 = None
    result = None
    error_message = None
    
    context = {}
    # The action to perform when submiting the form
    if request.method == 'POST':
        if 'action' in request.POST:
            action = request.POST['action']
            if action == 'btn_1':
                sql_syntax = request.POST.get('sql_syntax', '')
                try:
                    result = execute_sql(sql_syntax)
                except pymysql.Error as e:
                    error_message = str(e)
                context['result'] = result
    with connection.cursor() as cursor:        
        cursor.execute(f"""SELECT v.id, v.nom_ville, COUNT(*) AS Nbr_spectacle FROM ville v
                            JOIN spectacle s ON s.ville_id=v.id GROUP BY ville_id ORDER BY Nbr_spectacle, v.id;
                        """)
        extra_2= cursor.fetchall()
    context['extra_2'] = extra_2

    return render(request, 'extra2.html', context)

def extra3(request):
    extra_3 = None
    result = None
    error_message = None
    
    context = {}
    # The action to perform when submiting the form
    if request.method == 'POST':
        if 'action' in request.POST:
            action = request.POST['action']
            if action == 'btn_1':
                sql_syntax = request.POST.get('sql_syntax', '')
                try:
                    result = execute_sql(sql_syntax)
                except pymysql.Error as e:
                    error_message = str(e)
                context['result'] = result
    with connection.cursor() as cursor:        
        cursor.execute(f"""SELECT id AS id_hotel, nbr_room,
                            CASE 
                                WHEN hr.etat="Oc" 
                                THEN "Tout occupe" 
                            END AS etat
                        FROM (SELECT nbr_room, id, ville_id FROM hotel) AS h 
                        JOIN (SELECT COUNT(*) AS room_dispo, hotel_id, etat FROM hotel_room 
                        WHERE etat="Oc" GROUP BY hotel_id) AS hr 
                        ON hr.hotel_id=h.id WHERE h.nbr_room=hr.room_dispo;
                    """)
        extra_3 = cursor.fetchall()
    context['extra_3'] = extra_3

    return render(request, 'extra3.html', context)

def extra4(request):
    extra_4 = None
    result = None
    error_message = None
    
    context = {}
    # The action to perform when submiting the form
    if request.method == 'POST':
        if 'action' in request.POST:
            action = request.POST['action']
            if action == 'btn_1':
                sql_syntax = request.POST.get('sql_syntax', '')
                try:
                    result = execute_sql(sql_syntax)
                except pymysql.Error as e:
                    error_message = str(e)
                context['result'] = result
    with connection.cursor() as cursor:        
        cursor.execute(f"""SELECT h.id AS hotel, h.nbr_room AS Nbr_Total_Chambre, COUNT(*) Nbr_Chambre_Dispo
                            FROM hotel h
                            JOIN hotel_room hr ON h.id=hr.hotel_id
                            WHERE hr.etat="Li"
                            GROUP BY h.id;
                        """)
        extra_4 = cursor.fetchall()
    context['extra_4'] = extra_4

    return render(request, 'extra4.html', context)

def extra5(request):
    extra_5 = None
    result = None
    error_message = None
    
    context = {}
    # The action to perform when submiting the form
    if request.method == 'POST':
        if 'action' in request.POST:
            action = request.POST['action']
            if action == 'btn_1':
                sql_syntax = request.POST.get('sql_syntax', '')
                try:
                    result = execute_sql(sql_syntax)
                except pymysql.Error as e:
                    error_message = str(e)
                context['result'] = result
    with connection.cursor() as cursor:        
        cursor.execute(f"""SELECT h.id AS id_hotel, s.id as id_spectacle, 
                            CASE
                                WHEN s.ville_id = h.ville_id THEN
                                    CONCAT_WS(' ', ROUND(SQRT(POWER(s.loc_X - h.loc_X, 2) + POWER(s.loc_Y - h.loc_Y, 2)), 1), 'm')
                                ELSE CONCAT_WS(' ', ROUND(SQRT(POWER(h.loc_X, 2) + POWER(h.loc_Y, 2)) + SQRT(POWER(s.loc_X, 2) + POWER(s.loc_Y, 2)) + d.dist, 1), 'm')
                            END AS "Distance"
                        FROM distance d 
                        JOIN ville v1 ON d.id_ville1=v1.id
                        JOIN ville v2 ON d.id_ville2=v2.id
                        JOIN hotel h ON v1.id=h.ville_id OR v2.id=h.ville_id
                        JOIN spectacle s ON v1.id=s.ville_id OR v2.id=s.ville_id 
                        GROUP BY h.id, s.id, Distance order by h.id, s.id;
                    """)
        extra_5 = cursor.fetchall()
    context['extra_5'] = extra_5

    return render(request, 'extra5.html', context)

def extra6(request):
    extra_6 = None
    result = None
    error_message = None
    
    context = {}
    # The action to perform when submiting the form
    if request.method == 'POST':
        if 'action' in request.POST:
            action = request.POST['action']
            if action == 'btn_1':
                sql_syntax = request.POST.get('sql_syntax', '')
                try:
                    result = execute_sql(sql_syntax)
                except pymysql.Error as e:
                    error_message = str(e)
                context['result'] = result
    with connection.cursor() as cursor:        
        cursor.execute(f"""SELECT s.hotel, s.spectacle, s.Distance FROM (SELECT h.id AS hotel, s.id as spectacle,
                        	CASE
                        		WHEN s.ville_id = h.ville_id THEN
                        			CONCAT_WS(' ', ROUND(SQRT(POWER(s.loc_X - h.loc_X, 2) + POWER(s.loc_Y - h.loc_Y, 2)), 1), 'm')
                        		ELSE CONCAT_WS(' ', ROUND(SQRT(POWER(h.loc_X, 2) + POWER(h.loc_Y, 2)) + SQRT(POWER(s.loc_X, 2) + POWER(s.loc_Y, 2)) + d.dist, 1), 'm')
                        	END AS "Distance",
                        	CASE
                        		WHEN s.ville_id = h.ville_id THEN
                        			1
                        		ELSE 2
                        	END AS "Verif", h.ville_id as hotelvid, s.ville_id AS specvid
                        FROM distance d 
                        JOIN ville v1 ON d.id_ville1=v1.id
                        JOIN ville v2 ON d.id_ville2=v2.id
                        JOIN hotel h ON v1.id=h.ville_id OR v2.id=h.ville_id
                        JOIN spectacle s ON v1.id=s.ville_id OR v2.id=s.ville_id 
                        GROUP BY h.id, s.id, Distance order by h.id, s.id) AS s WHERE Verif=1;
                    """)
        extra_6 = cursor.fetchall()
    context['extra_6'] = extra_6

    return render(request, 'extra6.html', context)

def extra7(request):
    extra_7 = None
    result = None
    error_message = None
    
    context = {}
    # The action to perform when submiting the form
    if request.method == 'POST':
        if 'action' in request.POST:
            action = request.POST['action']
            if action == 'btn_1':
                sql_syntax = request.POST.get('sql_syntax', '')
                try:
                    result = execute_sql(sql_syntax)
                except pymysql.Error as e:
                    error_message = str(e)
                context['result'] = result
    with connection.cursor() as cursor:        
        cursor.execute(f"""SELECT h.id AS hotel, h2.id AS another_hotel, 
                            CASE
                                WHEN h.ville_id = h2.ville_id THEN
                                    CONCAT_WS(' ', ROUND(SQRT(POWER(h.loc_X - h2.loc_X, 2) + POWER(h.loc_Y - h2.loc_Y, 2)), 1), 'm')
                                ELSE CONCAT_WS(' ', ROUND(SQRT(POWER(h.loc_X, 2) + POWER(h.loc_Y, 2)) + SQRT(POWER(h2.loc_X, 2) + POWER(h2.loc_Y, 2)) + d.dist, 1), 'm')
                            END AS "Distance"
                        FROM distance d
                        JOIN ville v1 ON d.id_ville1=v1.id
                        JOIN ville v2 ON d.id_ville2=v2.id
                        JOIN hotel h ON v1.id=h.ville_id OR v2.id=h.ville_id
                        JOIN (SELECT id, ville_id, loc_X, loc_Y FROM hotel) AS h2 ON v1.id=h2.ville_id OR v2.id=h2.ville_id
                        GROUP BY h.id, h2.id, Distance order by h.id, h2.id;
                    """)
        extra_7 = cursor.fetchall()
    context['extra_7'] = extra_7

    return render(request, 'extra7.html', context)

def extra8(request):
    extra_8 = None
    result = None
    error_message = None
    
    context = {}
    # The action to perform when submiting the form
    if request.method == 'POST':
        if 'action' in request.POST:
            action = request.POST['action']
            if action == 'btn_1':
                sql_syntax = request.POST.get('sql_syntax', '')
                try:
                    result = execute_sql(sql_syntax)
                except pymysql.Error as e:
                    error_message = str(e)
                context['result'] = result
    with connection.cursor() as cursor:        
        cursor.execute(f"""SELECT s.id AS spectacle, s2.id AS another_spectacle, 
                            CASE
                                WHEN s.ville_id = s2.ville_id THEN
                                    CONCAT_WS(' ', ROUND(SQRT(POWER(s.loc_X - s2.loc_X, 2) + POWER(s.loc_Y - s2.loc_Y, 2)), 1), 'm')
                                ELSE CONCAT_WS(' ', ROUND(SQRT(POWER(s.loc_X, 2) + POWER(s.loc_Y, 2)) + SQRT(POWER(s2.loc_X, 2) + POWER(s2.loc_Y, 2)) + d.dist, 1), 'm')
                            END AS "Distance"
                        FROM distance d
                        JOIN ville v1 ON d.id_ville1=v1.id
                        JOIN ville v2 ON d.id_ville2=v2.id
                        JOIN spectacle s ON v1.id=s.ville_id OR v2.id=s.ville_id
                        JOIN (SELECT id, ville_id, loc_X, loc_Y FROM spectacle) AS s2 ON v1.id=s2.ville_id OR v2.id=s2.ville_id
                        GROUP BY s.id, s2.id, Distance order by s.id, s2.id;
                    """)
        extra_8 = cursor.fetchall()
    context['extra_8'] = extra_8

    return render(request, 'extra8.html', context)

def extra9(request):
    extra_9 = None
    result = None
    selected_date = None
    error_message = None
    form = forms.DateForm(request.POST)
    # selected_date = forms.DateForm(request.POST)
    
    context = {'form': form}
    # The action to perform when submiting the form
    if request.method == 'POST':
        if 'action' in request.POST:
            action = request.POST['action']
            if action == 'btn_1':
                sql_syntax = request.POST.get('sql_syntax', '')
                try:
                    result = execute_sql(sql_syntax)
                except pymysql.Error as e:
                    error_message = str(e)
                context['result'] = result
            elif action == 'btn_2':
                # DateField from django form
                if form.is_valid():
                    selected_date = form.cleaned_data['date_field']
                else:
                    form = forms.DateForm()
                with connection.cursor() as cursor:        
                    cursor.execute(f"""
                        SELECT s.id, s.name, s.categorie_spectacle FROM spectacle s
                        WHERE s.date_spectacle="{selected_date} 21:15:00";
                    """)
                    extra_9 = cursor.fetchall()
                context['selected_date'] = selected_date
                context['extra_9'] = extra_9

    return render(request, 'extra9.html', context)

def annuler(request):
    extra_9 = None
    result = None
    conf_annulation = None
    all_room = None
    annuler_id = None
    hotel_id = None
    hotel_name = None
    ville_name = None
    error_message = None
    
    context = {}
    # The action to perform when submiting the form
    if request.method == 'POST':
        if 'action' in request.POST:
            action = request.POST['action']
            if action == 'btn_1':
                sql_syntax = request.POST.get('sql_syntax', '')
                try:
                    result = execute_sql(sql_syntax)
                except pymysql.Error as e:
                    error_message = str(e)
                context['result'] = result
            elif action == 'btn_2':
                annuler_id = request.POST.get('annuler_id')
                if request.method == 'POST' and 'action' in request.POST:
                    action = request.POST['action']
                    if action == 'btn_3':
                        with connection.cursor() as cursor:
                            cursor.execute(f"DELETE FROM reservation r WHERE r.room_id={annuler_id}")
                        conf_annulation = cursor.fetchone()[0]

                
                with connection.cursor() as cursor:        
                    cursor.execute(f"""
                                        SELECT h.id as hotel FROM hotel_room hr JOIN hotel h ON h.id = hr.hotel_id
                                        WHERE hr.id={annuler_id};
                                    """)
                    hotel_id = cursor.fetchone()[0]
                with connection.cursor() as cursor:        
                    cursor.execute(f"""
                                        SELECT h.name FROM hotel h WHERE h.id={hotel_id};
                                    """)
                    hotel_name = cursor.fetchone()[0]
                with connection.cursor() as cursor:        
                    cursor.execute(f"""
                                        SELECT v.nom_ville AS ville from hotel h JOIN ville v ON v.id = h.ville_id
                                        WHERE h.name="{hotel_name}";
                                    """)
                    ville_name = cursor.fetchone()[0]

        context['ville_name'] = ville_name
        context['conf_annulation'] = conf_annulation
        context['annuler_id'] = annuler_id
        context['hotel_id'] = hotel_id
        context['hotel_name'] = hotel_name



    return render(request, 'annuler_reservation.html', context)
    

def ann_reussi(request):
    
    return render(request, 'ann_reussi.html')


def execute_sql(sql_syntax):
    # Connect to MySQL database
    connection = pymysql.connect(host='localhost',
                                user='projet',
                                password='password',
                                database='base',
                                cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql_syntax)
            result = cursor.fetchall()
            return result
    finally:
        connection.close()

