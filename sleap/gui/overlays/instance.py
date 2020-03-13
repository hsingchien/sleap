"""
Module with overlay for showing instances.
"""
import attr

from sleap.gui.state import GuiState
from sleap.gui.widgets.video import QtVideoPlayer
from sleap.io.dataset import Labels


@attr.s(auto_attribs=True)
class InstanceOverlay:
    """Class for adding instances as overlays on video frames.

    Attributes:
        labels: The :class:`Labels` dataset from which to get overlay data.
        player: The video player in which to show overlay.
        state: Object used to communicate with application.
    """

    labels: Labels = None
    player: QtVideoPlayer = None
    state: GuiState = None

    def __attrs_post_init__(self):
        if self.state is None:
            raise ValueError(
                "InstanceOverlay initialized without application GuiState."
            )

    def add_to_scene(self, video, frame_idx):
        """Adds overlay for frame to player scene."""
        if self.labels is None:
            return

        lf = self.labels.find(video, frame_idx, return_new=True)[0]

        instances = lf.instances_to_show

        has_predicted = any((True for inst in instances if hasattr(inst, "score")))
        has_user = any((True for inst in instances if not hasattr(inst, "score")))

        for instance in instances:
            self.player.addInstance(instance=instance)

        self.player.showLabels(self.state.get("show labels", default=True))
        self.player.showEdges(self.state.get("show edges", default=True))

        if has_user and has_predicted:
            self.player.highlightPredictions("not in training data")
