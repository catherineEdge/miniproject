import tkinter as tk
def bot():

    
    name = name_entry.get()
    problem=problem_entry.get()
    
    if problem.lower() in ["idk", "i dont know", "i don't know"]:
        result_text += "It's totally fine! Just tell me:\n- Acne\n- Stomach Pain\n- Fever\n- Headache"
    elif problem.lower() in ["rashes", "reshes", "rishes", "rashas"]:
        result_text +="Upload the picture\nApply lactic cream for 3 days\nDrink lots of water\nIf not better → meet doctor"
    else:
        result_text += f"I don't have a suggestion for '{problem}' yet."

   result_label.config(text=result_text)

    root=tk.Tk()
    root.title("health bot")
    root.geometry("400x500")
    root.resizable(False,False)
    root.configure(bg="lightblue")


def bot():
    name=input("your name:")
    print(f"starting {name}'s analysis....")
    problem=input("what problem are you are you facing")
    if problem.lower() in["idk" , "I dont know" , "i dont't know"]:
       print(f"it's totally fine {name} just tell me""\nacne?""\nstomach pain?" "\n fever? " "\n headache?")
    else:
        if problem.lower() in["rashes","reshes","rishes","rashas"]: 
            print("upload the picture") 
            print("apply lactic cream for 3 days")
            print("drink lots of water")
            print("should feel better for now if not decrease meet doctor")


bot()