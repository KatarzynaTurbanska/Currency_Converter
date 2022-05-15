import xmltodict
import urllib.request
import tkinter as tk
import tkinter.ttk as ttk

class App(tk.Frame):
    def __init__(self, master=None):
        """Initialize GUI window."""
        super().__init__(master)
        self.master = master
        self.master.title("Currency Converter (Katarzyna Turbańska)")
        self.master.geometry('505x150')
        self.master.configure(bg="#add8e6")

        self.get_data()
        self.labels()
        self.parameters()
        self.buttons()

    def get_data(self):
        """Get the exchange rates from Narodowy Bank Polski and save it in .xml file."""
        try:
            resource = urllib.request.urlopen("https://api.nbp.pl/api/exchangerates/tables/a?format=xml")
            content = resource.read()
            xmlFile = 'exchange_rate.xml' 
            with open(xmlFile, 'b+w') as openXml:
                openXml.write(content)
        except urllib.error.URLError:
            xmlFile = 'exchange_rate.xml'

        with open(xmlFile, encoding = 'utf-8') as fd:
            self.rates = {}
            self.rates[('polski złoty', 'PLN')] = 1
            doc = xmltodict.parse(fd.read())
            for x in range(len(doc['ArrayOfExchangeRatesTable']['ExchangeRatesTable']['Rates']['Rate'])):
                currency = doc['ArrayOfExchangeRatesTable']['ExchangeRatesTable']['Rates']['Rate'][x]['Currency']
                code = doc['ArrayOfExchangeRatesTable']['ExchangeRatesTable']['Rates']['Rate'][x]['Code']
                mid = doc['ArrayOfExchangeRatesTable']['ExchangeRatesTable']['Rates']['Rate'][x]['Mid']
                self.rates[(currency, code)] = mid

    def labels(self):
        """Create labels."""
        tk.Label(self.master, text="Amount", fg="black", bg="#add8e6", font='bold').place(x=0, y=0, width=75, height=30)
        tk.Label(self.master, text="From", fg="black", bg="#add8e6", font='bold').place(x=155, y=0, width=55, height=30)
        tk.Label(self.master, text="To", fg="black", bg="#add8e6", font='bold').place(x=355, y=0, width=35, height=30)

    def parameters(self):
        """Create places to input parameters needed to converting."""
        self.v_amount = tk.DoubleVar(self.master, value=1.0)
        tk.Entry(self.master, textvariable=self.v_amount, justify='center').place(x=0, y=40, width=150, height=30)
        
        self.v_from = ttk.Combobox(self.master, values = self.exchange_rate(), justify='center')
        self.v_from.current(0)
        self.v_from.place(x=155, y=40, width=150, height=30)

        self.v_to = ttk.Combobox(self.master, values = self.exchange_rate(), justify='center')
        self.v_to.current(2)
        self.v_to.place(x=355, y=40, width=150, height=30)

        self.value_error = tk.Label(self.master, text = '', bg="#add8e6")
        self.value_error.place(x=0, y=75, height=15)

        self.converted_label = tk.Label(self.master, text='', bg="#add8e6")
        self.converted_label.place(x=0, y=100)

    def buttons(self):
        """Create button to start converting, button to rotate 'From' and 'To' currencies, button to close application."""
        tk.Button(self.master, text="Convert", fg="black", bg="white", activebackground="#87cefa", command=self.convert_button).place(x=425, y=80, width=80, height=30)
        self.bn_quit = tk.Button(text='Quit', bg="white", command=self.master.quit).place(x=425, y=120, width=80, height=30) 

        image = tk.PhotoImage(file="rot.png")
        rotate_button = tk.Button(self.master, image=image, command=self.rotation)
        rotate_button.image = image
        rotate_button.place(x=310,y=40)

    def convert_button(self):
        """Convert the source currency into the target currency."""
        try:
            amount = self.v_amount.get()
            current_from = self.v_from.get()
            current_to = self.v_to.get()

            if amount > 0:
                amount = round(amount, 2)
                self.v_amount.set(amount)
                rate = self.rates[current_from.split(',')[0], current_from.split(', ')[1]]
                rate_to = self.rates[current_to.split(',')[0], current_to.split(', ')[1]]
                self.converted = round((float(rate)/float(rate_to))*amount, 2)
                self.converted_label.config(text="{} {} = {} {}".format(amount, current_from.split(', ')[1], self.converted, current_to.split(', ')[1]), font=("bold", 20))
                self.value_error.config(text="")
            else:
                self.value_error.config(text="Please enter an amount greater than 0", fg="red")
                self.converted_label.config(text="")
        except:
            self.value_error.config(text="Please enter a valid amount", fg="red")
            self.converted_label.config(text="")

    def exchange_rate(self):
        """"Returns the list of currencies."""
        exchange_rate_keys = []
        for (k, v) in self.rates.items():
            exchange_rate_keys.append(k[0] + ', ' + k[1])
        return exchange_rate_keys

    def rotation(self):
        """Switch the source currency with the target currency."""
        rot_from = self.v_from.get()
        rot_to = self.v_to.get()

        self.v_from.set(rot_from)
        self.v_to.set(rot_to)

if __name__ == '__main__':
    root = tk.Tk()
    app = App(master = root)
    app.mainloop()