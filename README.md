# IBMWatsonTest
Project to experiment some IBM Watson features

## What do you need
This program uses the IBM Watson Visual Recognition API for Python 2.7.
To install them use
```
pip install --upgrade watson-developer-cloud
```

## How to train a new classifier
To train from scratch a new classifier use command:

```
python training.py
```
This will use the default settings

or

```
python training.py -s <JSON settings file>
```

Before using this command fill the empty entries in the settings file.
By defining the field `"all_classes"` to  `true` in the settings file, the program will create a classifier with all the classes provided in the training file.
Otherwise if `"all_classes"` is `false` then only the classes defined in the field  `"classes"` will be considered.

## How to classify
To classify a [set of] image use the command 

```
python classify.py <image_id>
This will use the default settings

```
or

```
python classify.py <image_id> -s <JSON settings file>
```

if `<image_id>` refers to a `.txt` file the program will classify all the images defined in the file (see `input.txt` as an example)
