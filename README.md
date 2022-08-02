# milsboss
Software to control a Milsbo greenhouse cabinet
<div id="top"></div>

<!-- PROJECT HERO -->

<br />
<div align="center">
<!-- TODO: Find Logo
  <a href="">
    <img src="">
  </a>
 -->
  <h2 align="center">Milsboss</h2>

  <p align="center">
    Intelligently regulate the environment inside an Ikea Milsbo greenhouse cabinet to promote the health of exotic houseplants.
    <br />
    <br />
    <!-- TODO: Add demo link -->
    <!--
    <a href="">View Demo</a>
    ·
    -->
    <a href="https://github.com/kylejonesdev/milsboss/issues">Report Bug</a>
    ·
    <a href="https://github.com/kylejonesdev/milsboss/issues">Request Feature</a>
  </p>
</div>

<!-- TABLE OF CONTENTS -->
  <h3>Table of Contents</h3>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>


<!-- ABOUT THE PROJECT -->
## About The Project

<!-- TODO: Screenshot -->

Exotic plants grow best in an environment that mimics the environment in which they naturally grow. Simulating this environment requires specific light, humidity, and airflow conditions not commonly found in American households. Milsboss is a software package that uses a combination of custom timers and dynamic response to environmental conditions obtained through sensor readings in order to ensure that such an environment is maintained.

<p align="right">(<a href="#top">back to top</a>)</p>



## Features

* Polls greenhouse conditions at a custom time interval
* Maintains a weekly lighting schedule that can be customized for each day
* Reads internal humidity and intelligently responds, activating or deactivating the humidifier to ensure humidity is maintained within a desired range
* Activates fans at regular intervals to ensure air is not stagnant while minimizing fan noise
* Allows status updates and control of lights, fans, and humidifier via the popular mobile chat application Telegram


### Built With

This software is built entirely in Python.

Hardware required to effectively use the software includes:
* Raspberry Pi micro-computer
* Various I2C sensors from Adafruit.com to track greenhouse conditions
* A custom-built four outlet smart extension cord
* Led lighting, cooling fans, and a travel humidifier purchased online
* A closed environment, such as an Ikea Milsbo cabinet

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

- [x] Timed lighting by weekly schedule
- [x] Timed airflow at regular intervals
- [x] Dynamic, sensor-based humidity adjustment
- [x] Filterable hardware event logging in .csv format
- [x] Telegram status readouts and alerts
- [x] Telegram control of lighting, fans, and humidifier
- [ ] Readme file buildout
- [ ] Internal logging of program errors to logfile
- [ ] Overview of setup process and corresponding photos
- [ ] Code refactorin


See the [open issues](https://github.com/kylejonesdev/simple-books/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Do you love programming and plants? I'd **really appreciate** your contributions.

If you have a suggestion that would improve this project, please add an issue on the issues page of this repo or fork this repo and create a pull request.

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the GPL License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Kyle Jones - [@kylejonesdev](https://twitter.com/kylejonesdev) - [kylejones.dev](https://www.kylejones.dev/contact)

Project Link: [https://github.com/kylejonesdev/simple-books](https://github.com/your_username/repo_name)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

Here are just a few of the folks whose hard work really helped with this project:

* [othneildrew Readme Template](https://github.com/othneildrew/Best-README-Template)


<p align="right">(<a href="#top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
<!-- [React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/ -->