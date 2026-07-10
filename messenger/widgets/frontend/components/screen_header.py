from kivy.metrics import dp
from kivy.properties import StringProperty
from kivymd.uix.anchorlayout import MDAnchorLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.divider import MDDivider
from kivymd.uix.label import MDLabel
from .back_link import BackLink
from messenger.widgets.utils import bind_height_to_content_height, bind_height_to_texture_height

class ScreenHeader(MDBoxLayout):
    """ A Header for most Screens in the app.
        Provides a consistent themed look for Screens.
        Supports a primary title and an optional subtitle.
    """

    title = StringProperty('')
    subtitle = StringProperty('')

    def __init__(
            self,
            title='Screen Title',
            subtitle=None,
            back_link=True,
            back_loc='Home',
            **kwargs
    ):
        super(ScreenHeader, self).__init__(**kwargs)

        self.orientation = 'vertical'
        bind_height_to_content_height(self)

        # Horizontal container
        self.horizontal_container = MDBoxLayout(
            orientation='horizontal',
            spacing=dp(10),
        )
        bind_height_to_content_height(self.horizontal_container)
        self.add_widget(self.horizontal_container)

        # Back Link
        if back_link:
            self.back_link_container = MDAnchorLayout(anchor_y='top')
            self.back_link_container.size_hint_x = None
            self.horizontal_container.add_widget(self.back_link_container)
            self.back_link = BackLink(back_loc, icon='arrow-left')
            self.back_link_container.add_widget(self.back_link)

        # Headline Container
        self.headline_container = MDBoxLayout(orientation='vertical')
        bind_height_to_content_height(self.headline_container)
        self.horizontal_container.add_widget(self.headline_container)

        # Screen Title
        self.screen_title = MDLabel(text=title, font_style='Headline')
        bind_height_to_texture_height(self.screen_title)
        self.headline_container.add_widget(self.screen_title)

        # Screen Subtitle, Status Hint or Tooltip
        if subtitle:
            self.screen_subtitle = MDLabel(text=subtitle)
            bind_height_to_texture_height(self.screen_subtitle)
            self.headline_container.add_widget(self.screen_subtitle)

        # Divider
        self.divider = MDDivider()
        self.add_widget(self.divider)

    def on_title(self, _, title):
        self.screen_title.text = title

    def on_subtitle(self, _, subtitle):
        self.screen_subtitle.text = subtitle
