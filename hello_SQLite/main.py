# This project used https://www.youtube.com/watch?v=pd-0G0MigUA&ab_channel=CoreySchafer for reference
import sqlite_demo

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    sqlite_demo.create_table()
    from ui import window_controller
    window_controller.run_ui()
