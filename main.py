import GUI
import database_connector

database_connector.connect_to_mysql("localhost", "root", "8a8l8i8r8e8z8a8", "bank")
GUI.root_page()
database_connector.disconnect_to_mysql()
