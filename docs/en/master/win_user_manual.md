# Installing and Running EulerLauncher on Windows

EulerLauncher currently supports Windows 10/11. [Download the latest version of EulerLauncher][1] for Windows and decompress it to the desired location.
Right-click **config-env.bat** and choose **Run as administrator** from the shortcut menu. This script adds the current directory to the system environment variable `PATH`. If you know how to configure environment variables or the configuration script is incorrect, you can manually add the directory where the current script is located and the **qemu-img** subdirectory to the system environment variable `PATH`.

To run EulerLauncher on Windows, you need to connect EulerLauncher to the Hyper-V virtualization backend. Hyper-V is a Microsoft hardware virtualization product that provides better performance for VMs on Windows. Before running EulerLauncher, check whether Hyper-V is enabled in your system. For details about how to check and enable Hyper-V, see [Install Hyper-V][2] or other network resources.

The directory generated after the decompression contains the following files:

- **eulerlauncherd.exe**: main process of EulerLauncher. It is a daemon process running in the background. It interacts with various virtualization backends and manages the life cycles of VMs, containers, and images.
- **eulerlauncher.exe**: EulerLauncher CLI client. You can use this client to interact with the eulerlauncherd daemon process and perform operations on VMs and images.
- **eulerlauncher.conf**: EulerLauncher configuration file, which must be stored in the same directory as **eulerlauncherd.exe**. Configure the file as follows:

```ini
[default]
# Configure the directory for storing log files.
log_dir = D:\eulerlauncher-workdir\logs
# Whether to enable the debug log level.
debug = True
# Configure the EulerLauncher working directory.
work_dir = D:\eulerlauncher-workdir
# Configure the EulerLauncher image directory. The image directory is relative to the working directory.
image_dir = images
# Configure the VM file directory of EulerLauncher. The VM file directory is relative to the working directory.
instance_dir = instances
```

After the configuration is complete, right-click **eulerlauncherd.exe** and choose **Run as administrator** from the shortcut menu. **eulerlauncherd.exe** runs as a daemon process in the background.

Start PowerShell or Command Prompt to prepare for the corresponding operation.

## Exiting the eulerlauncherd Background Process on Windows

After **eulerlauncherd.exe** is executed, the eulerlauncherd icon is displayed in the system tray in the lower right corner. Right-click the icon and choose **Exit EulerLauncher** from the shortcut menu to exit the eulerlauncherd background process.

## Operations on Images

1. List available images.

    ```PowerShell
    eulerlauncher.exe images

    +-----------+----------+--------------+
    |   Images  | Location |    Status    |
    +-----------+----------+--------------+
    | 22.03-LTS |  Remote  | Downloadable |
    |   21.09   |  Remote  | Downloadable |
    | 2203-load |  Local   |    Ready     |
    +-----------+----------+--------------+
    ```

    There are two types of EulerLauncher images: remote images and local images. Only local images in the **Ready** state can be used to create VMs. Remote images can be used only after being downloaded. You can also load a downloaded local image to EulerLauncher. For details, see the following sections.

2. Download a remote image.

    ```PowerShell
    eulerlauncher.exe download-image 23.09

    Downloading: 23.09, this might take a while, please check image status with "images" command.
    ```

    The image download request is an asynchronous request. The download is completed in the background. The time required depends on your network status. The overall image download process includes download, decompression, and format conversion. During the download, you can run the `image` command to view the download progress and image status at any time.

    ```PowerShell
    eulerlauncher.exe images
    ```

    When the image status changes to **Ready**, the image is downloaded successfully. The image in the **Ready** state can be used to create VMs.

    ```PowerShell
    eulerlauncher.exe images
    ```

3. Load a local image.

    Load a custom image or an image downloaded to the local host to EulerLauncher to create a custom VM.

    ```PowerShell
    eulerlauncher.exe load-image --path {image_file_path} IMAGE_NAME
    ```

    The supported image formats are *xxx***.qcow2.xz** and *xxx***.qcow2**.

    Example:

    ```PowerShell
    eulerlauncher.exe load-image --path D:\openEuler-23.09-x86_64.qcow2.xz 2309-load

    Loading: 2309-load, this might take a while, please check image status with "images" command.
    ```

    Load the **openEuler-23.09-x86_64.qcow2.xz** file in the **D:\\** directory to the EulerLauncher system and name it **2309-load**. Similar to the download command, the load command is also an asynchronous command. You need to run the image list command to query the image status until the image status is **Ready**. Compared with directly downloading an image, loading an image is much faster.

    ```PowerShell
    eulerlauncher.exe images

    ......

    eulerlauncher images

    ......
    ```

4. Delete an image.

    Run the following command to delete an image from the EulerLauncher system:

    ```PowerShell
    eulerlauncher.exe delete-image 2309-load

    Image: 2309-load has been successfully deleted.
    ```

## Operations on VMs

1. List VMs.

    ```Powershell
    eulerlauncher.exe list

    +----------+-----------+---------+---------------+
    |   Name   |   Image   |  State  |       IP      |
    +----------+-----------+---------+---------------+
    |   test1  | 2309-load | Running | 172.22.57.220 |
    +----------+-----------+---------+---------------+
    |   test2  | 2309-load | Running |      N/A      |
    +----------+-----------+---------+---------------+
    ```

    If the VM IP address is **N/A** and the VM status is **Running**, the VM is newly created and the network configuration is not complete. Configuring the network takes several seconds. You can obtain the VM information again later.

2. Log in to a VM.

    If an IP address has been assigned to a VM, you can run the `ssh` command to log in to the VM.

    ```PowerShell
    ssh root@{instance_ip}
    ```

    If the official image provided by the openEuler community is used, the default username is **root** and the default password is **openEuler12#$**.

3. Create a VM.

    ```PowerShell
    eulerlauncher.exe launch --image {image_name} {instance_name}
    ```

    Use `--image` to specify an image and a VM name.

4. Delete a VM.

    ```PowerShell
    eulerlauncher.exe delete-instance {instance_name}
    ```

    Delete a specified VM based on the VM name.

[1]: https://gitee.com/openeuler/eulerlauncher/releases
[2]: https://learn.microsoft.com/en-us/virtualization/hyper-v-on-windows/quick-start/enable-hyper-v

