# Camera Software for OSS README

## Overview

Welcome to the Camera Software for OSS! This Python-based software seamlessly integrates with your cameras, capturing real-time availability information of sports spaces and sending it to the OSS.

## Features

- **Real-Time Availability:** Capture and transmit real-time data on the availability of sports spaces.

- **Integration:** Easy integration with various camera systems.

- **Authentication:** Secured by an authentication token obtained from OSS admin.

- **Data Security:** Ensure the security and privacy of captured data during transmission.

- **Raspberry Pi Compatibility:** Supports both Raspberry Pi camera (`F`) and other cameras (`T`).

## Getting Started

Follow these steps to get started with the Camera Software:

1. **Installation:** Clone this repository to your local machine.

   ```bash
   git clone https://github.com/Occupied-Sport-Space/people_counter
   ```

2. **Dependencies:** Install the necessary Python dependencies.

   ```bash
   pip install -r requirements.txt
   ```

3. **Authentication Token:** Request an authentication token from the OSS admin and save it in a `.env` file.

   ```dotenv
   AUTH_TOKEN=your_auth_token_here
   ```

4. **Space ID:** Obtain the space ID from the OSS admin.

5. **Update Configuration:** Update the `.env` file with the space ID.

   ```dotenv
   AUTH_TOKEN=your_auth_token_here
   SPACE_ID=your_space_id_here
   ```

6. **Run the Software:** Execute the `runCounter.sh` script with the first argument (`F` for Raspberry Pi camera, `T` for other cameras).

   ```bash
   ./runCounter.sh F  # for Raspberry Pi camera
   ./runCounter.sh T  # for other cameras
   ```

## Usage

The camera software will capture availability data and automatically send it to the OSS using the provided authentication token and space ID.

## Contribution

We welcome contributions! If you have any improvements or bug fixes, feel free to submit a pull request.

## License

This Camera Software is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Support

For any issues or inquiries, please contact our support team at occupiedsportspace@gmail.com.

Happy capturing! 📷🚀
