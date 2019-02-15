
from PIL import Image as _Image
import numpy as _np
from PIL import ImageDraw, ImageFont  
import colorsys
import numpy as np

import pathlib
from huasca import __file__ as _pkgrootfile
_rootpath = pathlib.PurePath(_pkgrootfile).parent

class Detection:
    """ Convenience object to contain detected object info. 
       Boxes follow PIL format of (left, upper, right, lower) 
       To be used with faces and generic objects. """
    
    @property
    def boxes(self):
        return self._boxes
    
    @property
    def scores(self):
        return self._scores

    @property
    def labels(self):
        return self._labels
    
    @property
    def base_image(self):
        return self._base_image

    @property
    def portraits(self):
        return [self.base_image.crop(self.pad_box(box,self._margin_ratio)) for box in self.boxes]

    @property
    def annotated(self):
        return self._annotate()
    
    def __init__(self,boxes,scores,labels,base_image):
        self._boxes = boxes
        self._scores = scores
        self._labels = labels

        if isinstance(base_image,_np.ndarray):
            base_image = _Image.fromarray(base_image)
        self._base_image = base_image

        self._margin_ratio = 0.1

    def set_padding(self,portrait_margin_ratio):
        """ How much margin to put around detection boxes """
        self._margin_ratio = portrait_margin_ratio

    def pad_box(self,box,margin_ratio = 0.1):
        """Pad a box size for context."""
        w = int(margin_ratio*(box[2]-box[0]))
        h = int(margin_ratio*(box[3]-box[1]))

        return (max(box[0]-w,0)
               ,max(box[1]-h,0)
               ,min(box[2]+w,self.base_image.size[0]) 
               ,min(box[3]+h,self.base_image.size[1])
                )

    def _annotate(self):
        image = self.base_image.copy()
        out_classes = self.labels

        # Generate colors for drawing bounding boxes.
        hsv_tuples = [(x / len(out_classes), 1., 1.)
                      for x in range(len(out_classes))]
        self._colors = list(map(lambda x: colorsys.hsv_to_rgb(*x), hsv_tuples))
        self._colors = list(
            map(lambda x: (int(x[0] * 255), int(x[1] * 255), int(x[2] * 255)),
                self._colors))
        np.random.seed(10101)  # Fixed seed for consistent colors across runs.
        np.random.shuffle(self._colors)  # Shuffle colors to decorrelate adjacent classes.
        np.random.seed(None)  # Reset seed to default.

        font = ImageFont.truetype(font=str(_rootpath.joinpath('bin/Arial.ttf')),
                    size=np.floor(3e-2 * image.size[1] + 0.5).astype('int32'))
        thickness = (image.size[0] + image.size[1]) // 300

        for i, c in reversed(list(enumerate(out_classes))):
            predicted_class = c
            box = self.boxes[i]
            box = [box[1],box[0],box[3],box[2]]
            score = self.scores[i]

            label = '{} {:.2f}'.format(predicted_class, score)
            draw = ImageDraw.Draw(image)
            label_size = draw.textsize(label, font)

            top, left, bottom, right = box
            top = max(0, np.floor(top + 0.5).astype('int32'))
            left = max(0, np.floor(left + 0.5).astype('int32'))
            bottom = min(image.size[1], np.floor(bottom + 0.5).astype('int32'))
            right = min(image.size[0], np.floor(right + 0.5).astype('int32'))
            print(label, (left, top), (right, bottom))

            if top - label_size[1] >= 0:
                text_origin = np.array([left, top - label_size[1]])
            else:
                text_origin = np.array([left, top + 1])

            # My kingdom for a good redistributable image drawing library.
            for t in range(thickness):
                draw.rectangle(
                    [left + t, top + t, right - t, bottom - t],
                    outline=self._colors[i])
            draw.rectangle(
                [tuple(text_origin), tuple(text_origin + label_size)],
                fill=self._colors[i])
            draw.text(text_origin, label, fill=(0, 0, 0), font=font)
            del draw

        return image

