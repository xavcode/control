

#* Function to get te selected item from the treeview and return the value 

def get_selected_item(treeview):
    item = treeview.selection()
    return treeview.item(item, "values")