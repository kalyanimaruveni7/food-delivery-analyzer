import gradio as gr

# ============================================================
#          LINKED LIST DATA STRUCTURE
# ============================================================

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, data):
        new = Node(data)
        if not self.head:
            self.head = new
            return
        temp = self.head
        while temp.next:
            temp = temp.next
        temp.next = new

    def display(self):
        temp = self.head
        result = []
        while temp:
            result.append(temp.data)
            temp = temp.next
        return result

    def search_restaurant(self, rest):
        temp = self.head
        result = []
        while temp:
            if temp.data["Restaurant"].lower() == rest.lower():
                result.append(temp.data)
            temp = temp.next
        return result

    def remove_by_id(self, oid):
        temp = self.head
        prev = None
        while temp and temp.data["OrderID"] != oid:
            prev = temp
            temp = temp.next
        if not temp:
            return False
        if prev is None:
            self.head = temp.next
        else:
            prev.next = temp.next
        return True

    def get_fastest(self):
        if not self.head:
            return None
        temp = self.head
        fastest = temp.data
        while temp:
            if temp.data["DeliveryTime"] < fastest["DeliveryTime"]:
                fastest = temp.data
            temp = temp.next
        return fastest

    def get_average(self):
        temp = self.head
        if not temp:
            return 0
        total, count = 0, 0
        while temp:
            total += temp.data["DeliveryTime"]
            count += 1
            temp = temp.next
        return round(total / count, 2)

    def high_value(self):
        temp = self.head
        result = []
        while temp:
            if temp.data["Price"] > 300:
                result.append(temp.data)
            temp = temp.next
        return result


# ============================================================
#                     INITIAL DATASET
# ============================================================

orders = LinkedList()

initial = [
    {"OrderID": 101, "Restaurant": "KFC", "Customer": "Arun", "Price": 320, "DeliveryTime": 28, "Location": "Chennai"},
    {"OrderID": 102, "Restaurant": "Dominos", "Customer": "Priya", "Price": 450, "DeliveryTime": 32, "Location": "Chennai"},
    {"OrderID": 103, "Restaurant": "Subway", "Customer": "Sanjay", "Price": 250, "DeliveryTime": 22, "Location": "Coimbatore"},
    {"OrderID": 104, "Restaurant": "KFC", "Customer": "Kumar", "Price": 500, "DeliveryTime": 45, "Location": "Madurai"},
    {"OrderID": 105, "Restaurant": "Dominos", "Customer": "Sita", "Price": 390, "DeliveryTime": 26, "Location": "Coimbatore"},
    {"OrderID": 106, "Restaurant": "Burger King", "Customer": "Lokesh", "Price": 280, "DeliveryTime": 35, "Location": "Chennai"},
    {"OrderID": 107, "Restaurant": "KFC", "Customer": "Anu", "Price": 310, "DeliveryTime": 21, "Location": "Madurai"},
]

for item in initial:
    orders.append(item)


# ============================================================
#                     BACKEND FUNCTIONS
# ============================================================

def show_all():
    return orders.display()

def search_restaurant(rest):
    return orders.search_restaurant(rest)

def add_order(oid, rest, cust, price, time, loc):
    try:
        data = {
            "OrderID": int(oid),
            "Restaurant": rest,
            "Customer": cust,
            "Price": float(price),
            "DeliveryTime": int(time),
            "Location": loc
        }
        orders.append(data)
        return "Order added successfully!"
    except:
        return "❌ Invalid input format"

def delete_order(oid):
    ok = orders.remove_by_id(int(oid))
    return "Deleted successfully!" if ok else "❌ Order ID not found"

def fastest():
    return orders.get_fastest()

def average():
    return orders.get_average()

def highvalue():
    return orders.high_value()


# ============================================================
#                 FRONTEND (GRADIO UI)
# ============================================================

with gr.Blocks() as app:
    gr.Markdown("# 🍔 Food Delivery Analyzer (Linked List Application)")

    with gr.Tab("Show All Orders"):
        out1 = gr.JSON()
        btn1 = gr.Button("Load All Orders")
        btn1.click(show_all, outputs=out1)

    with gr.Tab("Search by Restaurant"):
        rest = gr.Textbox(label="Restaurant Name")
        out2 = gr.JSON()
        btn2 = gr.Button("Search")
        btn2.click(search_restaurant, inputs=rest, outputs=out2)

    with gr.Tab("Add New Order"):
        oid = gr.Number(label="Order ID")
        r1 = gr.Textbox(label="Restaurant")
        c1 = gr.Textbox(label="Customer")
        p1 = gr.Number(label="Price")
        t1 = gr.Number(label="Delivery Time")
        l1 = gr.Textbox(label="Location")
        out3 = gr.Textbox()
        btn3 = gr.Button("Add Order")
        btn3.click(add_order, inputs=[oid, r1, c1, p1, t1, l1], outputs=out3)

    with gr.Tab("Delete Order"):
        delid = gr.Number(label="Order ID")
        out4 = gr.Textbox()
        btn4 = gr.Button("Delete")
        btn4.click(delete_order, inputs=delid, outputs=out4)

    with gr.Tab("Fastest Delivery"):
        out5 = gr.JSON()
        btn5 = gr.Button("Show Fastest")
        btn5.click(fastest, outputs=out5)

    with gr.Tab("Average Delivery Time"):
        out6 = gr.Textbox()
        btn6 = gr.Button("Show Average")
        btn6.click(average, outputs=out6)

    with gr.Tab("High Value Orders"):
        out7 = gr.JSON()
        btn7 = gr.Button("Show High Value Orders")
        btn7.click(highvalue, outputs=out7)

app.launch()
app.launch(share=True)