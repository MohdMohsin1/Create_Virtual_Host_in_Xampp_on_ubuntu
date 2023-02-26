#!/usr/bin/env python3

import os
import tkinter as tk
from tkinter import messagebox

class VirtualHostGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("XAMPP Virtual Host")
        self.master.resizable(False, False)
        self.master.geometry("400x200")

        # Create domain name input label and entry widget
        self.domain_name_label = tk.Label(self.master, text="Domain Name:")
        self.domain_name_label.pack()
        self.domain_name_entry = tk.Entry(self.master)
        self.domain_name_entry.pack()

        # Create document root input label and entry widget
        self.document_root_label = tk.Label(self.master, text="Document Root:")
        self.document_root_label.pack()
        self.document_root_entry = tk.Entry(self.master)
        self.document_root_entry.pack()

        # Create submit button
        self.submit_button = tk.Button(self.master, text="Submit", command=self.submit)
        self.submit_button.pack()

    def submit(self):
        domain_name = self.domain_name_entry.get()
        document_root = self.document_root_entry.get()

        # Create the virtual host configuration file
        config_file = "/opt/lampp/etc/extra/httpd-vhosts.conf"
        virtual_host = f"""
<VirtualHost *:80>
    ServerAdmin webmaster@{domain_name}
    DocumentRoot {document_root}
    ServerName {domain_name}
    ErrorLog /var/log/apache2/{domain_name}-error_log
    CustomLog /var/log/apache2/{domain_name}-access_log common
    <Directory "{document_root}">
        Options Indexes FollowSymLinks MultiViews
        AllowOverride All
        Order allow,deny
        Allow from all
        Require all granted
    </Directory>
</VirtualHost>
"""
        with open(config_file, "a") as file:
            file.write(virtual_host)

        # Add domain to hosts file
        hosts_file = "/etc/hosts"
        with open(hosts_file, "a") as file:
            file.write(f"127.0.0.1    {domain_name}\n")

        # Uncomment the virtual host in httpd.conf
        httpd_conf_file = "/opt/lampp/etc/httpd.conf"
        with open(httpd_conf_file, "r") as file:
            lines = file.readlines()
        with open(httpd_conf_file, "w") as file:
            for line in lines:
                if "#Include etc/extra/httpd-vhosts.conf" in line:
                    file.write(line.replace("#Include etc/extra/httpd-vhosts.conf", "Include etc/extra/httpd-vhosts.conf"))
                else:
                    file.write(line)

        # Restart XAMPP
        os.system("/opt/lampp/lampp restart")

        messagebox.showinfo("XAMPP Virtual Host", f"Virtual host for {domain_name} created successfully.")

if __name__ == "__main__":
    root = tk.Tk()
    app = VirtualHostGUI(root)
    root.mainloop()
