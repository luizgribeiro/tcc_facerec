from controllers.root_controller import RootController 
from controllers.webcam_controller import WebcamController
from views.display_atendees import DisplayAtendees
from views.webcam import Webcam



if __name__ == "__main__":
 
    App = RootController("Chamada Facial")

    webcam_contr = WebcamController(0)
    video = Webcam(App.get_window(),
                   webcam_contr.get_width(),
                   webcam_contr.get_height(),
                   webcam_contr.get_processed_frame,
                   15)
    disp_atendees = DisplayAtendees(App.get_window())
    App.run()