<img src="./logos/logo-slogan.png"/>

----

# EulerLauncher (Formerly OmniVirt)

Incubated by the technical operation team and infrastructure team of the openEuler community, **EulerLauncer** is a developer tool set integrating virtualization technologies (such as LXD, HyperV, and Virtualization Framework) in mainstream desktop OSs. It utilizes VMs and container images officially released by the openEuler community to provide developers with unified development resource (such as VMs and containers) provisioning and management on Windows, macOS, and Linux, improving the convenience and stability of using the openEuler development environment on mainstream desktop OSs, as well as developer experience.

*NOTE:* *EulerLauncher was formerly named as OmniVirt. Currently, related documents are being updated according to the new name.*

## Background

Convenient and stable development resources (such as VMs and containers) provided by mainstream desktop OSs are important to openEuler developers, especially for individuals and university developers who have limited resources. Common VM management platforms have many limitations. For examples, VirtualBox requires developers to download a large ISO image and install the OS simultaneously; WSL cannot provide a real openEuler kernel; most VM management software does not fully support Apple Sillicon chips, and a majority of them needs to be paid, all of which greatly hinder developers' efficiency.

**EulerLauncher** provides a convenient, easy-to-use, and unified developer tool set on mainstream desktop OSs such as Windows, macOS, and Linux (under planning). It supports the x86_64 and AArch64 hardware architectures, including Apple Silicon chips. It also delivers virtual hardware acceleration capabilities for different platforms, providing high-performance development resources. **EulerLauncher** allows developers to utilize VMs, container images (under planning), Daily Build images provided by the community, and other qualified custom images, thereby providing developers with a wide range of choices.

## Quick Start

For **EulerLauncher** MacOS users, see the [EulerLauncher User Guide for MacOS Users][1].
For **EulerLauncher** Windows users, see the [EulerLauncher User Guide for Windows Users][2].

[1]: ./docs/mac-user-manual.md
[2]: ./docs/win-user-manual.md