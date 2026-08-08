from flet import *

from data.manage_sprint_data import SprintData
from views.components.ItemFormInSprint import ItemFormInSprint
from views.components.LoadingCard import LoadingCard
from .components.ItemCard import ItemCard
from .components.ItemForm import ItemForm
from .components.SortPopupButton import SortPopupButton
from .components.FilterPopupButton import FilterPopupButton
from data.manage_data import Data
from data.filter_data import DataFilter 
from data.task_filter import TaskFilter
from data.task_sorter import TaskSorter
from data.color_data import ColourData
import asyncio

class SprintListView(Column):
    def __init__(self, page,):
        print("Sprint list view initialized")
        super().__init__()
        self.item_list = []
        self.page = page

        self.selected_tags = []

        self.filter_tag = "All Tasks"
        self.sort_label = "Oldest to Newest"

        # self.width = self.page.width - 330
        # self.height =  self.page.height - 20
        # self.bgcolor = "#CADEED"
        # self.border_radius = border_radius.all(10)
        # self.padding = padding.all(20)

    
        self.board = GridView(
            expand=1,
            max_extent=300,
            child_aspect_ratio=1.40,
            spacing=10,
            run_spacing=10,
            padding=padding.all(5),
        )

    def build_board(self, items=None):
        print("Building sprint backlog board")
        if items == []:
            return Container(
                content=Text("No items in the sprint backlog", color=colors.BLACK, size=20),
                alignment=alignment.center,
                expand=1,
            )
    
        elif items:

            self.board.controls.clear()
            for item in items:
                self.board.controls.append(
                    Container(
                        content=ItemCard(item_dict=item, handle_detailed_view=self.handle_detailed_view),
                        alignment=alignment.center,
                    )
                )
            return self.board
        
        else:
            return LoadingCard()


    def build(self):
        print("Building Sprint List View")
        
        self.filter_tag_row = Row(controls=[], alignment=MainAxisAlignment.START)
        return Container(
            content=Column([
                        Row([
                            Text("Sprint Backlog", color=colors.BLACK, size=40, weight=FontWeight.BOLD),
                            self.filter_tag_row,
                            Row([
                                SortPopupButton(self.handle_sort_option),
                                FilterPopupButton(self.filter_selected_tag),
                                IconButton(icon=icons.CLOSE, on_click=lambda e: self.page.go("/sprintboard"),tooltip="Close"),
                            ], alignment=MainAxisAlignment.END),
                        ], alignment=MainAxisAlignment.SPACE_BETWEEN),
                        Container(
                            content=self.build_board(),
                            alignment=alignment.center,
                            expand=1,
                        )
                    ], expand=True),
            padding=padding.all(20),
            border_radius=border_radius.all(10),
            bgcolor="#CADEED",
            width=self.page.width - 330,
            height=self.page.height - 60,
        )
    
    def before_update(self):
        if self.page.route.startswith("/sprintlist/"):

            print("\033[33mSprint List View updated\033[0m")
            sprint_id = self.page.route.split("/")[2]
            sprint_name = asyncio.run(SprintData().get_sprint_item(sprint_id))["sprint_name"]
            print("Sprint name:", sprint_name)
                
            self.controls[0].content.controls[0].controls[0].value = "Sprint Backlog Of " +  sprint_name

            self.controls[0].width = self.page.width - 330
            self.controls[0].height =  self.page.height - 60
            
            asyncio.run(self.populate_board(refetch=True))

    def did_mount(self):
        print("\033[33mSprint backlog mounted\033[0m")
        asyncio.run(self.load_initial_background_color())
        
    async def load_initial_background_color(self):
        color_item = await ColourData().get_color_items()  # Get color items
        for item in color_item:
            if item['component'] == "Sprint KanBan View":
                self.bgcolor = item['background_color']
                self.controls[0].bgcolor = self.bgcolor
                break
    
    async def populate_board(self, refetch=False):
        print("Populating board")

        if refetch:
            print("Fetching sprint backlog items")
            all_items = await (Data().get_product_backlog_items())

            print(self.page.route)
            sprint_id = self.page.route.split("/")[2]
            self.item_list = []
            for item in all_items:
                try:
                    if item["sprint_id"] == sprint_id:
                        self.item_list.append(item)
                except KeyError:
                    print("Item has no sprint_id")
            
        items = TaskSorter().sort_tasks(self.item_list, self.sort_label)
        items = TaskFilter().filter_task(self.item_list, self.selected_tags)
        self.controls[0].content.controls[1].content = self.build_board(items)
        print("Board populated")
    
    def handle_detailed_view(self, id):
        print("Detailed view clicked")
        for item in self.item_list:
            if item["_id"] == id:
                self.detailed_view = ItemFormInSprint(self.page, self.close_detailed_view, mode="view", item_dict=item)
                self.page.open(self.detailed_view)
                break

    def close_detailed_view(self):
        print("Closing detailed view")
        self.page.close(self.detailed_view)
        asyncio.run(self.populate_board(refetch=True))
        self.page.update()
    
    def handle_sort_option(self, sort_option):
        print("Sort option selected:", sort_option)
        self.sort_label = sort_option
        asyncio.run(self.populate_board())
        self.update()

    def filter_selected_tag(self, tag):
        print("Filter selected:", tag)
        
        if tag == "All Tasks":
            self.selected_tags = ["All Tasks"]
        else:
            if "All Tasks" in self.selected_tags:
                self.selected_tags.remove("All Tasks")
                
            if tag in self.selected_tags:
                self.selected_tags.remove(tag)
            else:
                self.selected_tags.append(tag)

        asyncio.run(self.populate_board())
        self.update_filter_tag_row(self.selected_tags)
        self.update()

    def change_bg_colour(self, selected_color):
        """Change the background color of the product backlog."""
        self.bg_color = selected_color
        self.controls[0].bgcolor = self.bg_color  # Update the container's background
        self.page.update()
        asyncio.run(ColourData().save_background_color("Product Backlog", self.bg_color))

    def create_tag_bubble(self, tag):
        """Creates a Chip control for the selected filter tag."""
        chip = Chip(
            label=Text(tag, color="black"),
            color="#DBEBE2",  # Background color for the chip
            border_side=BorderSide(color="white", width=1),
            delete_icon_color="black",
            on_delete=lambda e: self.remove_tag(tag),  
        )
        return chip
    
    def update_filter_tag_row(self, tags):
        """Updates the filter tag row with the current selected tag bubble."""
        # Clear previous tags
        self.filter_tag_row.controls.clear()
        
        # Add the new tag bubble
        for tag in tags:
            tag_bubble = self.create_tag_bubble(tag)
            self.filter_tag_row.controls.append(tag_bubble)

        # Refresh the page to show changes
        self.page.update()

    def remove_tag(self, tag):
        if tag in self.selected_tags:
            print(f"Removing filter tag: {tag}")
            self.selected_tags.remove(tag)
            self.update_filter_tag_row(self.selected_tags)  # Update displayed tags
            asyncio.run(self.populate_board())
            self.page.update()

