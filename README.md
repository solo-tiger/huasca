# Huasca

##### Computer vision models OOB (out-of-the-bottle).

                     __
                    [__]
       ___        .+'. '+.
       )_(       /:;/ _.+'\
       + +       +:._   .++
     .+'+'+.  _  |:._     |
    /+::_..+_[_]_+:._CV   |
    )_     /_   _\:._     |
    +;:    )_``'_(:._     +
    +;::+..+;:.._++.____.+'
    `+.._..`+...+'

Huasca enables prototyping by prioritizing generalization and rapid development over accuracy.

##### Step into the cellar and select a bottle of computer visions.

  * Face detection & localization
  * Face classification
    * age
    * gender
  * Object detection & localization
  * Object tracking
  * Object classification w/o localization

Face and object localization include convenient cropping and annotation methods to feed classifiers.

## Roadmap

  * v0.3.0 - reduce and combine models to save space
  * v0.4.x - add style transfer
  * v0.4.x - face recognition

## Examples

### Detection

Detection results include:

  * `boxes`: Boxes follow PIL format of (left, upper, right, lower)
    * top-left corner is (0,0) and offsets go down/right from there (physics indexing)
  * `scores`: confidence score for each detected object
  * `labels`: label description of the object e.g. ['dog','person']
  * `portraits`: cropped objects from base image (PIL.Image format)
  * `base_image`: the source image (PIL.Image format)
  * `annotated`: the source image with objects annotated (PIL.Image format)

#### Face & Object Detection

    # Get a PIL image from somewhere:
    image = ...
    
    # Use PIL image as input:
    import huasca

    faces   = huasca.detect.faces(image)
    objects = huasca.detect.objects(image)

    # Display the first face
    faces.portraits[0].show()
    
    # Check classes
    print(objects.labels)

    # Retrieve annotated & labeled version of either
    faces.annotated.show()
    objects.annotated.show()

#### Face Demographics

    # Get a PIL image of a face from face detector:
    face = faces.portraits[0]

    gender,age = huasca.classify.demographics(face)


### Object Tracking

    import huasca

    data = json.load(json_data)
    object_log = huasca.object_tracking.track_objects(data)
    output_json = [obj.to_json() for obj in object_log]
