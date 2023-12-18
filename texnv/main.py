import tkinter as tk
from tkinter import ttk
from tkinter import Text, Scrollbar
import psycopg2

conn = psycopg2.connect(
            dbname='it175120', user='it175120',
            password='658072', host='dblabs.iee.ihu.gr'
        )
    

def add_player():
    
    # team_id = team_id_entry.get()
    surname = surname_entry.get()
    name = name_entry.get()
    nationality = nationality_entry.get()
    height = height_entry.get()
    position = position_entry.get()

    
    # success = add_player_to_db(team_id, surname, name, nationality, height, position)
    success = add_player_to_db(surname, name, nationality, height, position)
    if success:
        print("Player added successfully")
    else:
        print("Failed to add player")


def edit_team():
    
    team_name = team_name_entry.get()
    new_team_coach = new_team_coach_entry.get()

    
    success = edit_team_info_in_db(team_name, new_team_coach) 
    if success:
        print("Team information edited successfully")
    else:
        print("Failed to edit team information")


def delete_player():
    
    player_name = delete_player_name_entry.get()

    
    success = delete_player_by_name_from_db(player_name)
    if success:
        print("Player deleted successfully")
    else:
        print("Failed to delete player")


def search_team():
    team_name = search_team_entry.get()
    team_info = get_team_info_from_db(team_name)

    if team_info:
        
        team_info_text.config(state="normal")
        team_info_text.delete("1.0", tk.END)
        team_info_text.insert(tk.END, team_info)
        team_info_text.config(state="disabled")
    else:
        team_info_text.config(state="normal")
        team_info_text.delete("1.0", tk.END)
        team_info_text.insert(tk.END, "Team not found.")
        team_info_text.config(state="disabled")


def get_team_info_from_db(team_name):
    try:
        cursor = conn.cursor()
        sql = f"""
          SELECT t.team_name, c.firstname 
            FROM TEAMS t 
            JOIN COACHES c ON t.coach_fk = c.coach_id 
            WHERE t.team_name = %s

        """
        
        cursor.execute(sql,(team_name,))
        team_data = cursor.fetchall()
        cursor.close()

       ## if not team_data:
        ##c    return None

        team_info = f"Team Name: {team_data[0][0]}\n"
        team_info += f"Team Coach: {team_data[0][1]}\n\n"
        team_info += "Players:\n"
        # for player in team_data:
        #     if player[2]:
        #         team_info += f"- {player[2]}\n"
        # team_info += "\nCoaches:\n"
        # for coach in team_data:
        #     if coach[3]:
        #         team_info += f"- {coach[3]}\n"

        return team_info

    except psycopg2.Error as e:
        print("Error retrieving team information:", e)
        return None


def add_player_to_db(surname, name, nationality, height, position):
    try:
        cursor = conn.cursor()
        sql = "INSERT INTO players ( surname, first_name, nationality, height, poss) VALUES ( %s, %s, %s, %s, %s)"
        cursor.execute(sql, ( surname, name, nationality, height, position))
        conn.commit()
        cursor.close()
        return True
    except psycopg2.Error as e:
        print("Error adding player:", e)
        return False


def edit_team_info_in_db(team_name, new_team_coach):
    try:
        cursor = conn.cursor()
        sql = "UPDATE TEAMS SET coach_fk = %s WHERE team_name = %s"
        cursor.execute(sql, (new_team_coach, team_name))
        conn.commit()
        cursor.close()
        return True
    except psycopg2.Error as e:
        print("Error editing team information:", e)
        return False


def delete_player_by_name_from_db(player_name):
    try:
        cursor = conn.cursor()
        sql = "DELETE FROM PLAYERS WHERE first_name = %s"
        cursor.execute(sql, (player_name,))
        conn.commit()
        cursor.close()
        return True
    except psycopg2.Error as e:
        print("Error deleting player:", e)
        return False


root = tk.Tk()
root.title("Basketball Data Management")


window_width = 443
window_height = 750
root.geometry(f"{window_width}x{window_height}")


canvas = tk.Canvas(root)
canvas.pack(fill="both", expand=True)


scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
scrollbar.pack(side="right", fill="y")
canvas.configure(yscrollcommand=scrollbar.set)


frame = tk.Frame(canvas, bg="light green")
canvas.create_window((0, 0), window=frame, anchor="nw")


add_player_label = tk.Label(frame, text="Add Player", font=("Arial", 16, "bold"))
add_player_label.pack(pady=10)


# team_id_label = tk.Label(frame, text="Team ID:")
# team_id_label.pack()
# team_id_entry = tk.Entry(frame)
# team_id_entry.pack()

surname_label = tk.Label(frame, text="Surname:")
surname_label.pack()
surname_entry = tk.Entry(frame)
surname_entry.pack()

name_label = tk.Label(frame, text="Name:")
name_label.pack()
name_entry = tk.Entry(frame)
name_entry.pack()

nationality_label = tk.Label(frame, text="Nationality:")
nationality_label.pack()
nationality_entry = tk.Entry(frame)
nationality_entry.pack()

height_label = tk.Label(frame, text="Height:")
height_label.pack()
height_entry = tk.Entry(frame)
height_entry.pack()

position_label = tk.Label(frame, text="Position:")
position_label.pack()
position_entry = tk.Entry(frame)
position_entry.pack()

add_player_button = ttk.Button(frame, text="Add Player", command=add_player)
add_player_button.pack()


edit_team_label = tk.Label(frame, text="Edit Team Information", font=("Arial", 16, "bold"))
edit_team_label.pack(pady=10)


team_name_label = tk.Label(frame, text="Team Name:")
team_name_label.pack()
team_name_entry = tk.Entry(frame)
team_name_entry.pack()

new_team_coach_label = tk.Label(frame, text="New Coach:")
new_team_coach_label.pack()
new_team_coach_entry = tk.Entry(frame)
new_team_coach_entry.pack()

edit_team_button = ttk.Button(frame, text="Edit Team", command=edit_team)
edit_team_button.pack()


delete_player_label = tk.Label(frame, text="Delete Player", font=("Arial", 16, "bold"))
delete_player_label.pack(pady=10)


delete_player_name_label = tk.Label(frame, text="Player Name to Delete:")
delete_player_name_label.pack()
delete_player_name_entry = tk.Entry(frame)
delete_player_name_entry.pack()

delete_player_button = ttk.Button(frame, text="Delete Player", command=delete_player)
delete_player_button.pack()


search_team_frame = tk.Frame(frame)
search_team_frame.pack(side="right", padx=20, fill="both", expand=True)

search_team_label = tk.Label(search_team_frame, text="Search Team", font=("Arial", 16, "bold"))
search_team_label.pack()

search_team_entry = tk.Entry(search_team_frame)
search_team_entry.pack()

search_team_button = ttk.Button(search_team_frame, text="Search Team", command=search_team)
search_team_button.pack(pady=5)


team_info_text = Text(search_team_frame, wrap=tk.WORD, width=50, height=10, state="disabled")
team_info_text.pack(pady=10, fill="both", expand=True)


frame.update_idletasks()
canvas.configure(scrollregion=canvas.bbox("all"))


root.mainloop()


conn.close()