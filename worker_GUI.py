v=1
import tkinter as tk 
from tkinter import ttk
import webview
import requests
import threading
import json
import os

if not os.path.exists("keys"):
    with open("keys", "w") as f:
        f.write("Delete This or paste somthing" + "\n" + "Delete This or paste somthing")
root=tk.Tk()
root.geometry("500x500")
def hand2(event):
    event.widget.config(cursor="hand2")
def c_cloud():
    webview.create_window("cloudflare" , "https://cloudflare.com")

    webview.start()

def del_workers():
    def delete_worker(api_token, account_id, worker_name):
        """Delete a Cloudflare Worker."""
        url = f'https://api.cloudflare.com/client/v4/accounts/{account_id}/workers/scripts/{worker_name}'

        headers = {
            'Authorization': f'Bearer {api_token}',
            'Content-Type': 'application/json'
        }

        response = requests.delete(url, headers=headers)

        if response.status_code == 200:
            print(f'Worker "{worker_name}" deleted successfully.')
            none= True
        else:
            print(f'Failed to delete worker: {response.status_code} - {response.text}')
            none= False
        for w in root.winfo_children():
            w.pack_forget()
        if none==True:
            show_la=ttk.Label(root, text=f'Worker "{worker_name}" deleted successfully.')
            show_la.pack(pady=15,ipadx=50)
        else:
            show_la=ttk.Label(root, text=f'Worker "{worker_name}" did not delete.')
            show_la.pack(pady=15,ipadx=50)  
            

        save_button=ttk.Button(root, text="OK" ,command=main)
        save_button.pack() 
     
    def getname():

        with open("keys" , "r") as f :
                w=f.readlines()
        api_token=w[0]
        api_token=api_token[:len(api_token)-1]
        account_id=w[1]
        delete_worker(api_token, account_id, get_na.get())
    def theard_get_na():
        therrd=threading.Thread(target=getname)
        therrd.start()
    for w in root.winfo_children():
            w.pack_forget()

    del_la=ttk.Label(root, text="Worker name to delete: ")
    del_la.pack(pady=15,ipadx=50)


    get_na=ttk.Entry(root)
    get_na.pack(pady=15,ipadx=50)

    del_fu=ttk.Button(root, text="Go" ,command=theard_get_na)
    del_fu.pack()
    
    le=ttk.Button(root, text="Go back" ,command=main)
    le.pack()



def list_workers(api_token, account_id):
    """List all Cloudflare Workers."""
    workers="Loading .... "
    for w in root.winfo_children():
            w.pack_forget()
    account_id_label=ttk.Label(root, text=f"{workers} ")
    account_id_label.pack(pady=15,ipadx=50)
    try:
        url = f'https://api.cloudflare.com/client/v4/accounts/{account_id}/workers/scripts'

        headers = {
            'Authorization': f'Bearer {api_token}',
            'Content-Type': 'application/json'
        }

        response = requests.get(url, headers=headers)
        a="None"
        if response.status_code == 200:
            workers = response.json()['result']
            if workers:
                print("List of workers:")
                a=""
                for worker in workers:
                    a+=f"- {worker['id']}"+"\n"
                
            else:
                print("No workers found.")
            
        else:
            print(f'Failed to list workers: {response.status_code} - {response.text}')
            workers=" None"
    except Exception:
        workers="None"

    account_id_label.config(text=f"{a} ")

    save_button=ttk.Button(root, text="OK" ,command=main)
    save_button.pack() 
    
def list_workers_go( ):
    with open("keys" , "r") as f :
        w=f.readlines()
    api_token=w[0]
    api_token=api_token[:len(api_token)-1]
    account_id=w[1]
    list_workers(api_token, account_id)
def theard_list_workers_go():
    theard=threading.Thread(target=list_workers_go)
    theard.start()
def without_kv(api_token, account_id,worker_name):

    def go(script):
                script_url=script
                def fetch_worker_script(script_url):
                    """Fetch the worker script from a given URL."""
                    response = requests.get(script_url)
                    if response.status_code == 200:
                        return response.text
                    else:
                        print(f"Failed to fetch worker script: {response.status_code} - {response.text}")
                        return None
                def get_workers_dev_subdomain(api_token, account_id):
                    """Retrieve the workers.dev subdomain for the Cloudflare account."""
                    url = f'https://api.cloudflare.com/client/v4/accounts/{account_id}/workers/subdomain'

                    headers = {
                        'Authorization': f'Bearer {api_token}',
                        'Content-Type': 'application/json'
                    }

                    response = requests.get(url, headers=headers)

                    if response.status_code == 200:
                        subdomain = response.json()['result']['subdomain']
                        print(f'Workers.dev subdomain retrieved: {subdomain}')
                        return subdomain
                    else:
                        print(f'Failed to retrieve workers.dev subdomain: {response.status_code} - {response.text}')
                        return None
                def publish_worker_on_workers_dev(api_token, account_id, worker_name):
                    """Publish the worker on the workers.dev subdomain."""
                    url = f'https://api.cloudflare.com/client/v4/accounts/{account_id}/workers/scripts/{worker_name}/subdomain'

                    headers = {
                        'Authorization': f'Bearer {api_token}',
                        'Content-Type': 'application/json'
                    }

                    data = {"enabled": True}

                    response = requests.post(url, headers=headers, json=data)  # Changed from PUT to POST

                    if response.status_code == 200:
                        print(f'Worker "{worker_name}" published on workers.dev subdomain successfully.')
                        return True
                    else:
                        print(f'Failed to publish worker on workers.dev subdomain: {response.status_code} - {response.text}')
                        return False
                def create_worker(api_token, account_id, worker_name, script, kv_namespace_id, variable_name):
                    """Create or update a Cloudflare Worker."""
                    url = f'https://api.cloudflare.com/client/v4/accounts/{account_id}/workers/scripts/{worker_name}'

                    headers = {
                        'Authorization': f'Bearer {api_token}',
                    }

                    bindings = []
                    if kv_namespace_id and variable_name:
                        bindings = [
                            {
                                "name": variable_name,
                                "namespace_id": kv_namespace_id,
                                "type": "kv_namespace"
                            }
                        ]

                    # Prepare the metadata with bindings and specify module type (ESM)
                    metadata = {
                        "main_module": "worker.js",
                        "type": "esm",  # For ES module
                        "bindings": bindings
                    }

                    # Prepare the files for the multipart upload
                    files = {
                        'metadata': ('metadata', json.dumps(metadata), 'application/json'),
                        'worker.js': ('worker.js', script, 'application/javascript+module'),
                    }

                    response = requests.put(url, headers=headers, files=files)

                    if response.status_code == 200:
                        if kv_namespace_id and variable_name:
                            print(f'Worker {worker_name} created/updated successfully and bound to KV namespace with variable name "{variable_name}".')
                        else:
                            print(f'Worker {worker_name} created/updated successfully without KV namespace binding.')
                        return True
                    else:
                        print(f'Failed to create/update worker: {response.status_code} - {response.text}')
                        return False
                script=fetch_worker_script(script)

                if script:
                            subdomain = get_workers_dev_subdomain(api_token, account_id)
                            if subdomain:
                                if create_worker(api_token, account_id, worker_name, script, kv_namespace_id=None, variable_name=None):
                                    if publish_worker_on_workers_dev(api_token, account_id, worker_name):
                                            def copt_url(event):
                                                root.clipboard_append(f"https://{worker_name}.{subdomain}.workers.dev/panel")
                                                url.config(text="Copied")
                                            url=ttk.Label(root,style="Costumpp.TLabel", text=f"Click to copy :\n\nhttps://{worker_name}.{subdomain}.workers.dev/panel" , cursor="hand2")
                                            url.pack(fill=tk.X,pady=5)
                                            url.bind("<Button-1>" ,copt_url)
                                            leeve_button=ttk.Button(root, text="Go Back" ,command=main)
        
    def went_go():
        go(script_url_name.get())
    for w in root.winfo_children():
        w.pack_forget()
    script_url_name_label=ttk.Label(root, text="worker Script url : ")
    script_url_name_label.pack(pady=15,ipadx=50)
    script_url_name=ttk.Entry(root)
    script_url_name.pack(pady=15,ipadx=50)
    save_buttonw2=ttk.Button(root, text="Go" ,command=went_go)
    save_buttonw2.pack()
    leeve_button=ttk.Button(root, text="Go Back" ,command=main)
    leeve_button.pack(pady=5)

    root.mainloop() 
    
def create():
    def check():
        if checkbox_var.get() == 0:
             
            without_kv(api_token.get(), account_id.get(),worker_name.get())
       
        else:
            print("bye bye")
        def create_kv_namespace(api_token, account_id, kv_namespace_name):
            def go_final():
                def end_create():
                    def fetch_worker_script(script_url):
                        def show_go_another():
                            def get_workers_dev_subdomain(api_token, account_id):
                                bb=False
                                bb2=False
                                def publish_worker_on_workers_dev(api_token, account_id, worker_name):
                                        global bb2
                                        """Publish the worker on the workers.dev subdomain."""
                                        url = f'https://api.cloudflare.com/client/v4/accounts/{account_id}/workers/scripts/{worker_name}/subdomain'

                                        headers = {
                                            'Authorization': f'Bearer {api_token}',
                                            'Content-Type': 'application/json'
                                        }

                                        data = {"enabled": True}

                                        response = requests.post(url, headers=headers, json=data)  # Changed from PUT to POST

                                        if response.status_code == 200:
                                            print(f'Worker "{worker_name}" published on workers.dev subdomain successfully.')
                                            bb2= True
                                        else:
                                            print(f'Failed to publish worker on workers.dev subdomain: {response.status_code} - {response.text}')
                                            bb2= False
                                
                                def get_publish_worker_on_workers_dev():
                                    publish_worker_on_workers_dev(api_token, account_id, worker_name.get())
                                def theard_get_publish_worker_on_workers_dev():
                                    theard=threading.Thread(target=get_publish_worker_on_workers_dev)
                                    theard.start()
                                
                                def create_worker(api_token, account_id, worker_name, script, kv_namespace_id, variable_name):
                                    print(api_token, account_id, worker_name, script, kv_namespace_id, variable_name)
                                    global bb

                                        
                                    """Create or update a Cloudflare Worker."""
                                    url = f'https://api.cloudflare.com/client/v4/accounts/{account_id}/workers/scripts/{worker_name}'

                                    headers = {
                                        'Authorization': f'Bearer {api_token}',
                                    }

                                    bindings = []
                                    if kv_namespace_id and variable_name:
                                        bindings = [
                                            {
                                                "name": variable_name,
                                                "namespace_id": kv_namespace_id,
                                                "type": "kv_namespace"
                                            }
                                        ]

                                    # Prepare the metadata with bindings and specify module type (ESM)
                                    metadata = {
                                        "main_module": "worker.js",
                                        "type": "esm",  # For ES module
                                        "bindings": bindings
                                    }

                                    # Prepare the files for the multipart upload
                                    files = {
                                        'metadata': ('metadata', json.dumps(metadata), 'application/json'),
                                        'worker.js': ('worker.js', script, 'application/javascript+module'),
                                    }

                                    response = requests.put(url, headers=headers, files=files)

                                    if response.status_code == 200:
                                        if kv_namespace_id and variable_name:
                                            print(f'Worker {worker_name} created/updated successfully and bound to KV namespace with variable name "{variable_name}".')
                                        else:
                                            print(f'Worker {worker_name} created/updated successfully without KV namespace binding.')
                                        bb= True
                                    else:
                                        print(f'Failed to create/update worker: {response.status_code} - {response.text}')
                                        bb= False
                                    return bb
                                def get_create_worker():
                                    with open("keys" , "r") as f :
                                        w=f.readlines()
                                    api_token=w[0]
                                    api_token=api_token[:len(api_token)-1]
                                    account_id=w[1]
                                    bb= create_worker(api_token, account_id, worker_name.get(), response2.text, namespace_id, variable_name.get() )
                                    return  bb 
                                
                                """Retrieve the workers.dev subdomain for the Cloudflare account."""
                                url = f'https://api.cloudflare.com/client/v4/accounts/{account_id}/workers/subdomain'

                                headers = {
                                    'Authorization': f'Bearer {api_token}',
                                    'Content-Type': 'application/json'
                                }

                                response = requests.get(url, headers=headers)

                                if response.status_code == 200:
                                    subdomain = response.json()['result']['subdomain']
                                    print(f'Workers.dev subdomain retrieved: {subdomain}')
                                    
                                else:
                                    print(f'Failed to retrieve workers.dev subdomain: {response.status_code} - {response.text}')
                                    subdomain= None
                                if subdomain != None:
                                    bb= get_create_worker()
                                    
                                    if bb != False:
                                        bb2=publish_worker_on_workers_dev(api_token, account_id, worker_name.get())
                                        if bb2 != False:
                                            for w in root.winfo_children():
                
                                                w.pack_forget()

                                            
                                            """Generate the default workers.dev URL for the worker."""
                                            def copt_url(event):
                                  
                                                root.clipboard_append(f"https://{worker_name.get()}.{subdomain}.workers.dev/panel")
                                                url.config(text="Copied")

                                            url=ttk.Label(root,style="Costumpp.TLabel", text=f"Click to copy :\n\nhttps://{worker_name.get()}.{subdomain}.workers.dev/panel" , cursor="hand2")
                                            url.pack(fill=tk.X,pady=5)
                                            url.bind("<Button-1>" ,copt_url)

                                            leeve_button=ttk.Button(root, text="Go Back" ,command=main)
                                            leeve_button.pack(pady=5) 

                            def get_get_workers_dev_subdomain():
                                with open("keys" , "r") as f :
                                    w=f.readlines()
                                api_token=w[0]
                                api_token=api_token[:len(api_token)-1]
                                account_id=w[1]
                                get_workers_dev_subdomain(api_token , account_id)
                            def theard_get_get_workers_dev_subdomain():
                                theard=threading.Thread(target=get_get_workers_dev_subdomain)
                                theard.start()
                                   
                            if response2 != None:
                                theard_get_get_workers_dev_subdomain()


                        """Fetch the worker script from a given URL."""
                        response2 = requests.get(script_url)
                        if response.status_code == 200:
                            pass
                        else:
                            print(f"Failed to fetch worker script: {response2.status_code} - {response2.text}")
                            response2= None

                        show_go_another()
                    fetch_worker_script(script_url_name.get())
                def get_end_create():

                        end_create()
                def theard_get_end_create():
                        theard=threading.Thread(target=get_end_create)
                        theard.start()
                    
                for w in root.winfo_children():
                
                    w.pack_forget()

                script_url_name_label=ttk.Label(root, text="worker Script url : ")
                script_url_name_label.pack(pady=15,ipadx=50)

    

                script_url_name=ttk.Entry(root)
                script_url_name.pack(pady=15,ipadx=50)

                save_buttonw2=ttk.Button(root, text="Go" ,command=theard_get_end_create)
                save_buttonw2.pack()

                leeve_button=ttk.Button(root, text="Go Back" ,command=main)
                leeve_button.pack(pady=5) 
            if checkbox_var.get() == 0:
                go_final()
                
            namespace_id="loading"
            lab_ch=ttk.Label(root, text=f"{namespace_id}")
            lab_ch.pack(pady=15,ipadx=50)
            for w in root.winfo_children():
                w.pack_forget()
            
            """Create a KV namespace and return its ID."""
            url = f'https://api.cloudflare.com/client/v4/accounts/{account_id}/storage/kv/namespaces'

            headers = {
                'Authorization': f'Bearer {api_token}',
                'Content-Type': 'application/json'
            }

            data = {
                "title": kv_namespace_name
            }

            response = requests.post(url, headers=headers, json=data)

            if response.status_code == 200:
                namespace_id = response.json()['result']['id']
                print(f'KV namespace "{kv_namespace_name}" created successfully with ID: {namespace_id}')
             
            else:
                print(f'Failed to create KV namespace: {response.status_code} - {response.text}')
                namespace_id= None
            if namespace_id!=None:
                go_final()                     
        def get_create_kv_namespac():
                for w in root.winfo_children():
                    w.pack_forget()
                load=ttk.Label(root, text="Loading ... ")
                load.pack(pady=15,ipadx=50)
                with open("keys" , "r") as f :
                    w=f.readlines()
                api_token=w[0]
                api_token=api_token[:len(api_token)-1]
                account_id=w[1]
                kv_n=kv_namespace_name.get()
                create_kv_namespace(api_token , account_id, kv_n)
        def theard_get_kv_namespec():
            theard=threading.Thread(target=get_create_kv_namespac)
            theard.start()
                
        for w in root.winfo_children():
            w.pack_forget()
        if checkbox_var.get()==1:
                kv_namespace_name_label=ttk.Label(root, text="Enter the desired KV namespace name: ")
                kv_namespace_name_label.pack(pady=15,ipadx=50)

    

                kv_namespace_name=ttk.Entry(root)
                kv_namespace_name.pack(pady=15,ipadx=50)

                variable_name_label=ttk.Label(root, text="Enter the desired variable name for the KV namespace binding:  ")
                variable_name_label.pack(pady=15,ipadx=50)

                

                variable_name=ttk.Entry(root)
                variable_name.pack(pady=15,ipadx=50)

                go_button=ttk.Button(root, text="Go" ,command=get_create_kv_namespac)
                go_button.pack()

                leeve_button=ttk.Button(root, text="Go Back" ,command=main)
                leeve_button.pack(pady=5) 
        else:
            get_create_kv_namespac()

    for w in root.winfo_children():
            w.pack_forget()
    worker_name_label=ttk.Label(root, text="Enter the desired worker name: ")
    worker_name_label.pack(pady=15,ipadx=50)

    

    worker_name=ttk.Entry(root)
    worker_name.pack(pady=15,ipadx=50)

    style.configure("TCheckbutton",
                        indicatorcolor="blue",
                        indicatorsize=5,
                        padding=5)
    
    style2=ttk.Style()
    style2.configure("C.TLabel",
                        foreground="darkgreen")

    worker_name_label=ttk.Label(root, text="Do you want to create a KV namespace? ")
    worker_name_label.pack(pady=15,ipadx=50)

    checkbox_var=tk.IntVar(value=1)
    checkbox1 = ttk.Checkbutton(root, text="yes", variable=checkbox_var, onvalue=1, offvalue=0)
    checkbox1.pack(ipady=5,anchor=tk.CENTER)
    checkbox1.bind("<Enter>", hand2)

    checkbox2 = ttk.Checkbutton(root, text="no", variable=checkbox_var, onvalue=0, offvalue=0)
    checkbox2.pack(ipady=5,anchor=tk.CENTER)
    checkbox2.bind("<Enter>", hand2)

    save_button=ttk.Button(root, text="Go" ,command=check)
    save_button.pack()

    leeve_button=ttk.Button(root, text="Go Back" ,command=main)
    leeve_button.pack(pady=5) 
     
def main():
    with open("keys" , "w") as f:
        f.write(api_token.get()+"\n")
        f.write(account_id.get())
    
    for w in root.winfo_children():
            w.pack_forget()
    button_List_Workers=ttk.Button(root, text="List Workers" ,command=theard_list_workers_go)
    button_List_Workers.pack(fill=tk.BOTH,pady=15)

    button_Create_Worker=ttk.Button(root, text="Create Worker" ,command=create)
    button_Create_Worker.pack(fill=tk.BOTH,pady=15)

    button_Delete_Worker=ttk.Button(root, text="Delete Worker" ,command=del_workers)
    button_Delete_Worker.pack(fill=tk.BOTH,pady=15)
style3 = ttk.Style(root)
style3.configure("c.TLabel",
                            foreground="red",
                            background="#ffffff",
                            highlightthickness=20,
                            highlightbackground="lightblue",
                            padding=10,
                            highlightcolor="lightblue",
                            relief="groove",
                            font=("Helvetica", 10, "bold"),
                            anchor="center",
                            justify="center")
vpn=ttk.Label(root, style="c.TLabel",text="Use VPN please! ")
vpn.pack(pady=15,ipadx=50)   
fram=tk.Frame(root,width=400,height=300)

fram.pack()

with open("keys" , "r") as f :
    w=f.readlines()
api_token=w[0]
api_token=api_token[:len(api_token)-1]
account_id=w[1]

ent_var=tk.StringVar(value=api_token)
ent_var2=tk.StringVar(value=account_id)

style = ttk.Style(root)
style.configure("TButton",
                    foreground="#848484",
                    background="lightblue",
                    highlightthickness=20,
                    highlightbackground="lightblue",
                    highlightcolor="lightblue",
                    relief="groove",
                    padding=5,
                    borderwidth=0,
                    bordercolor="lightblue",
                    font=("Helvetica", 12, "bold"),
                    anchor="center",
                    justify="center")


button=ttk.Button(fram, text="Open cloudflare", command=c_cloud)
button.pack(pady=5, fill=tk.X)


                
style = ttk.Style(root)
                
style.configure("TEntry",
         
                
    foreground="#3d7e7d",
                
    highlightthickness=20,
                
    highlightbackground="lightblue",
                
    highlightcolor="lightblue",
                
    font=("Helvetica", 10),
                
    anchor="center",
                
    justify="center",
                
    )
style2=ttk.Style(root)
style2.configure("TLabel",
                            foreground="#3d7e7d",
                            background="#ffffff",
                            highlightthickness=20,
                            highlightbackground="lightblue",
                            padding=10,
                            highlightcolor="lightblue",
                            relief="groove",
                            font=("Helvetica", 10, "bold"),
                            anchor="center",
                            justify="center")


api_token_label=ttk.Label(root, text="Enter Api token ")
api_token_label.pack(pady=15,ipadx=50)

api_token=ttk.Entry(root, textvariable=ent_var)

api_token.pack(pady=15,ipadx=50)

style2=ttk.Style(root)
style2.configure("TLabel",
                            foreground="#3d7e7d",
                            background="#ffffff",
                            highlightthickness=20,
                            highlightbackground="lightblue",
                            padding=10,
                            highlightcolor="lightblue",
                            relief="groove",
                            font=("Helvetica", 10, "bold"),
                            anchor="center",
                            justify="center")
account_id_label=ttk.Label(root, text="Enter Account Id : ")
account_id_label.pack(pady=15,ipadx=50)

account_id=ttk.Entry(root, textvariable=ent_var2)
account_id.pack(pady=15,ipadx=50)

save_button=ttk.Button(root, text="Save" ,command=main)
save_button.pack()

create_by=ttk.Label(root, text="\nThis app was created by arshiacomplus\nand forked from koland")
create_by.pack(pady=15,ipadx=50)
root.mainloop()
