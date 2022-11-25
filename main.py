# from voters import *
# from admin import *
import maskpass
import sqlite3
import os


# -----PREQUESTITES TO KNOW
# pip install maskpass
#  admin username : admin
#  admin password : admin
#  ON FIRST RUN UNCOMMENT THE (RUN ONLY ONCE PART)


# connecting the databases
connAd = sqlite3.connect("candidate.sqlite")
conn = sqlite3.connect("voter.sqlite")
curAd = connAd.cursor()
cur = conn.cursor()

# ------------------------------------------------------------------
# VOTERS PART


class Voter:

    '''
    Attributes:
        voter_id(string)
        name(string)
    '''
    # Constructor

    def __init__(self, voter_id, name, age, gender):
        self.voter_id = voter_id
        self.name = name
        self.age = age
        self.gender = gender


# Inherited Class
class VoteStatus(Voter):
    def __init__(self, voter_id, name, age, gender, area, vote_status):
        super().__init__(voter_id, name, age, gender)
        self.area = area
        self.vote_status = vote_status

    def __repr__(self):
        return (self.voter_id, self.name, self.age, self.gender, self.area, self.vote_status)


# DATABASE PART
# create script
create_script = '''
CREATE TABLE voter (voter_id INT PRIMARY KEY,
name VARCHAR(30) NOT NULL,
age INT NOT NULL,
gender VARCHAR(10),
area VARCHAR(20),
vote_status VARCHAR(7))
'''

# creating the database
# EXECUTE ONLY ONCE ON THE FIRST RUN  #       (RUN ONLY ONCE ON FIRST RUN)
#cur.execute(create_script)


# making variables for insertion

# COMMENT OUT THIS TABLE IF YOU WANT TO ADD DATA MANUALLY  #       (RUN ONLY ONCE ON FIRST RUN)
# (USE ON FIRST RUN IF THE TABLE IS EMPTY)


# -----------------------------------------------------------------------------


# -------------------------------------------------------------------------------------
# ADMIN PART

# class definitions
class candidateBase:
    def __init__(self, candiate_id, name):
        self.candidate_id = candiate_id
        self.name = name


class candidate(candidateBase):
    def __init__(self, candidate_id, name, area, votes_recieved):
        super().__init__(candidate_id, name, area, votes_recieved)
        self.area = area
        self.votes_recieved = votes_recieved

    def __repr__(self):
        return (self.candidate_id, self.name, self.area, self.votes_recieved)


# Create script
create_scriptAd = '''
CREATE TABLE candidate (
    candidate_id INT PRIMARY KEY,
    name VARCHAR(100),
    area VARCHAR(20),
    votes_recieved INT
)
'''

# creating the database       #     (RUN ONLY ONCE ON FIRST RUN)
# curAd.execute(create_scriptAd)
# print("Successfully created the table")
# --------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------
# MAIN MENU

# Greeting message
print("--------------------------------")
print(f'HELLO! WELCOME TO OUR E-VOTING SERVICE')
print("--------------------------------")

# USER SELECTION
print("CHOOSE YOUR USER-TYPE:")
try:
    print(("""1.Voter\n2.Admin\n"""))
    option = int(input("Choose your option: "))
    option = int(option)
    if type(option) != type(1):
        raise TypeError("Invalid Option")
    elif (option != 1 & option != 2):
        raise ValueError("Option doesnt exist")
except TypeError:
    print("WRONG INPUT!")
except ValueError:
    print("THE OPTION DOESNT EXIST")

# Interface for the admin
if option == 2:
    os.system("cls")
    print("WELCOME TO THE ADMIN PANEL:")
    print("\nLogin to the system: ")
    userName = input("Username: ")
    password = maskpass.askpass(prompt="Password: ", mask="*")

    # admin credentials checking
    try:
        if (userName != "admin" or password != "admin"):
            raise KeyError("Wrong login credentials")
        else:

            print("---------------------------\n")
            print("WELCOME TO THE ADMIN PANEL")
            print("---------------------------\n")

            # Admin panel options
            print("ADMIN ACTIONS: ")
            print("1. Add candidate\n")
            print("2. Remove candidate\n")
            print("3. Modify candidate\n")
            print("4. Display candidate data\n")
            print("5. Reveal Winner\n")
            print("6. Reset all\n")

            # Admin action implementation
            adminOption = int(input("\nChoose your option: "))

            # adding candidate
            if (adminOption == 1):
                os.system("cls")
                candidate_id = int(input("Enter the candidate's ID: "))
                candidate_name = (
                    input("Enter the candidate's name: ")).upper()
                candidate_area = (
                    input("Enter the candidate's area: ")).upper()
                candidate_voteCount = 0
                insert_scriptAd = f'''
                INSERT INTO candidate VALUES (?,?,?,?)
                '''
                curAd.execute(insert_scriptAd, (candidate_id,
                              candidate_name, candidate_area, candidate_voteCount))
                print("\nSuccessfully added the candidate")

            # removing the candidate
            elif (adminOption == 2):
                os.system("cls")
                candidate_id = int(
                    input("Enter the Candidate ID who you want to remove: "))

                # Selecting the voter row from id to remove
                candidateIdDeleteScript = f'''DELETE FROM candidate WHERE candidate_id = {candidate_id}'''
                curAd.execute(candidateIdDeleteScript)
                print("\nSuccessfully deleted the candidate\n")

            # Modify Candidate
            elif (adminOption == 3):
                os.system("cls")
                candidate_id = int(
                    input("Enter the ID of candidate who you want to modify: "))
                newCandidateName = input(
                    "Enter the new name of candidate: ").upper()
                newCandidateArea = input(
                    "Enter the new area of candidate: ").upper()

                # selecting the candidate and then modifying with new values
                candidateUpdateScript = f'''
                UPDATE candidate SET name = ?, area = ? WHERE candidate_id = {candidate_id}
                '''
                curAd.execute(candidateUpdateScript,
                              (newCandidateName, newCandidateArea))
                print("\nSuccessfully updated modified the candidate details")

            # Display all the data of candidates
            elif (adminOption == 4):
                candidateDisplayAllScript = '''SELECT * FROM candidate'''
                candidateDump = curAd.execute(candidateDisplayAllScript)
                print("ID\tName\t\t Area\t\tVote Count")
                for row in candidateDump:
                    print(f"{row[0]}\t{row[1]}", " " *
                          (15-len(row[1])), f"{row[2]}\t{row[3]}")

            # Revealing the winner of election
            elif (adminOption == 5):
                winnerRevealScript = '''
                SELECT candidate_id,name,area, votes_recieved 
                FROM candidate 
                WHERE votes_recieved = (SELECT MAX(votes_recieved) FROM candidate) AND votes_recieved > 0'''
                winner = curAd.execute(winnerRevealScript)
                candidate = curAd.fetchall()
                os.system("cls")
                print("The winner of the election is/are: \n")
                for winner in candidate:
                    print(
                        f"{winner[1]} from {winner[2]} of ID {winner[0]}\n with total votes of {winner[3]}")
            # Resetting the election, setting vote count to 0
            elif (adminOption == 6):
                resetScript = '''UPDATE candidate SET votes_recieved = 0'''
                curAd.execute(resetScript)
                resetScript = '''UPDATE voter SET vote_status = "FALSE"'''
                cur.execute(resetScript)
                print("Successfully resetted the votes count")

            else:
                print("\n! Wrong option !")

    except KeyError:
        print("\n! Wrong username/password !")


# Interface for the voters
elif option == 1:
    os.system('cls')
    print("-------------------WELCOME TO THE ELECTRONIC VOTING MACHINE------------------------")
    print("\nSome rules to follow while voting:\n")
    print("1.You can vote only for one candidate.\n")
    print("2.You can vote only the candidates from your area.\n")
    print("3.Your vote will be anonymous, but verbal discretion after voting would be your responsibility.\n")
    print(f"----------------IMPORTANT NOTICE------------------\n\nVOTES WILL BE COUNTED ON THE FIRST TRY\n\nIF YOU MAKE AN INVALID OPTION, YOUR VOTE WON'T BE COUNTED\n")
    matchingID = int(input("Enter your voter ID: "))

    voterIdFilterScript = f'''
    SELECT vote_status, voter_id, area 
    FROM voter 
    WHERE voter_id = {matchingID} AND vote_status = "FALSE"'''

    # Match the table with voter id and return the id, status and area
    filteredRow = cur.execute(voterIdFilterScript)
    rows = cur.fetchall()
    voterList = []
    for filteredRow in rows:
        voterList.append(filteredRow)
    print(voterList)
    if (len(voterList) != 0):
        votingArea = [tup[2] for tup in voterList][0]
        # print(votingArea)
    else:
        os.system("cls")
        print("Such voter ID doesnt exist or you have already voted\n\n")

    # Updating the vote status to true to prevent duplicate votes from same voter
    updateScript = f''' UPDATE voter SET vote_status = "TRUE" WHERE voter_id = {matchingID} '''
    cur.execute(updateScript)

    # filtering to view candidates from the same area as voter
    candidateFilterScript = f'''SELECT candidate_id, name FROM candidate WHERE area = "{votingArea}"'''
    filteredCandidates = curAd.execute(candidateFilterScript)
    candidates = curAd.fetchall()
    candidateList = []
    for filteredCandidates in candidates:
        candidateList.append(filteredCandidates)

    # displaying the candidates
    if (len(candidateList) != 0):
        candidateListCodes = [tup[0] for tup in candidateList]
        candidateListNames = [tup[1] for tup in candidateList]

        os.system('cls')
        print("Candidates from your area: ")
        print("ID\tNAME")
        for index in range(len(candidateListCodes)):
            print(f"{candidateListCodes[index]}\t{candidateListNames[index]}")

        vote = int(input("Enter the id of candidate who you want to vote for: "))
        if (vote not in candidateListCodes):
            print("Wrong Candidate Code.\nYour vote is invalid")
        else:
            votedCandidateScript = f'''UPDATE candidate SET votes_recieved = votes_recieved+1 WHERE candidate_id = {vote}'''
            curAd.execute(votedCandidateScript)
            os.system("cls")
            print("Successfully voted. \nThank you for voting")
    else:
        print("\nNo candidates from your area")


conn.commit()
connAd.commit()
connAd.close()
conn.close()
