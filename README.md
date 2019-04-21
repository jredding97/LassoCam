# LassoCam

LassoCam is an automated presentation assistant that uses computer vision to track the presenter. In its current form, it uses a Raspberry Pi with a Pimoroni Pantilthat holding a PiCamera. The user selects a presenter upon launch, which will then be tracked using the OpenCV library. The system is paired with a remote, which consists of a laser and three buttons - Laser, Lasso, and Home. The Laser button acts as a standard laser pointer. When the Lasso button is pressed, a window appears allowing a selection to be made. The camera will focus on that location until the Home button is pressed on the remote, at which point it will return the presenter.

## Getting Started

Clone the LassoCam repository to your device.

Install prerequisites (listed below, will add detail)

Run the LassoCam.py program

### Prerequisites

OpenCV - Newest Versioning
	-- OpenCV Python (Contrib)
	-- All OpenCV prerequisites (Will detail later)
Python 3
[pySerial] (https://pythonhosted.org/pyserial/)
[imutils] (https://github.com/jrosebr1/imutils) -- Can be installed with pip

Raspberry Pi 3B+
Pimoroni PanTiltHat
PiCamera
Logitech C920

### Installing

```
See Getting Started
```

## Deployment

This system is not currently ready for live deployment.

## Built With

* [OpenCV](http://www.dropwizard.io/1.0.2/docs/) - The web framework used
* [Python](https://maven.apache.org/) - Dependency Management
* [PySerial](https://rometools.github.io/rome/) - Used to generate RSS Feeds

## Contributing

Not currently accepting public contributions

## Authors

* **John Redding** - *Main Program* - [Museus](https://github.com/Museus)
* **Mike Cannizaaro** - *Hardware Design* - [MikeC96](https://github.com/MikeC96)
* **Andrew Dodel** - *Angle Calculation* - [andrewdodel](https://github.com/andrewdodel)
* **Alex McMullen** - *User Interface* - [AlexanderTheDecent](https://github.com/AlexanderTheDecent)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* [PyImageSearch](https://www.pyimagesearch.com) tutorials were incredibly helpful
* [Adrian Rosebrock's](https://github.com/jrosebr1) imutils library made initial development much easier

