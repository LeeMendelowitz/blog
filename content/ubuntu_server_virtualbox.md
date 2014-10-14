Title: Ubuntu Server Virtual Machine with SSH using VirtualBox on Mac OS X
Date: 2014-10-13 12:00
Slug: ubuntu-server-virtualbox
Category: misc
Tags: Ubuntu, VirtualBox
Author: Lee Mendelowitz
Summary: How to set up an Ubuntu Server guest virtual machine on OS X in Virtual Box

My laptop is a late 2011 MacBook Pro running OS X 10.9 Mavericks. It's my personal laptop, so I use it for everything - browsing, e-mail, and programming. While the OS X experience is wonderful, application development can be frustrating. For example, right now I'm trying to develop a Boost Python module, and I am having trouble compiling it on OS X.

I intend to run my application in a Linux environment, so instead of learning the intricacies of porting my code and makefile to Mac OS X, I decided to install a local Ubuntu Server virtual machine (VM) on my MacBook. I installed Ubuntu Server instead of Ubuntu Desktop because I wanted to run a lightweight Linux environment, which should save laptop resources. I simply run the VM in the background, and ssh into it from the Mac terminal. Easy and awesome!

** This entire tutorial should take approximately 20 minutes (not including download times). **

## Install VirtualBox

Download and install VirtualBox [here](https://www.virtualbox.org/wiki/Downloads). The
instructions below were testing with VirtualBox 4.3.18 on OS X 10.9.5.

## Download Ubuntu

Download the [Ubuntu Server 14.04.01 LTS](http://www.ubuntu.com/download/server) iso image. 

## Setting up the Virtual Machine (VM)

You can configure your virtual machine (VM) using the VirtualBox graphical program, but it's quicker to set it up from the command line. I've adapted these commands in part from this [blog post](http://www.perkin.org.uk/posts/create-virtualbox-vm-from-the-command-line.html).

The commands below will create a virtual machine called "UbuntuServer",
attach a 32 GB virtual hard drive, attach a DVD
drive loaded with the Ubuntu Server disk image, and allocate 1 GB of RAM. We also 
attach a network card and set up port forwarding. 

<!-- All of these settings can be easily changed in the future (except expanding the virtual hard ddrive size is kind of tricky because you'll have to [resize the drive partition](http://www.howtogeek.com/124622/how-to-enlarge-a-virtual-machines-disk-in-virtualbox-or-vmware/)). If you are curious, you can read more about these vboxmanage commands by referring to the [VirtualBox documentation](https://www.virtualbox.org/manual/ch08.html). -->

```bash

cd ~/VirtualBox\ VMs/

# Change these variables as needed
VM_NAME="UbuntuServer"
UBUNTU_ISO_PATH=~/Downloads/ubuntu-14.04.1-server-amd64.iso
VM_HD_PATH="UbuntuServer.vdi" # The path to VM hard disk (to be created).
SHARED_PATH=~ # Share home directory with the VM


vboxmanage createvm --name $VM_NAME --ostype Ubuntu_64 --register
vboxmanage createhd --filename $VM_NAME.vdi --size 32768
vboxmanage storagectl $VM_NAME --name "SATA Controller" --add sata --controller IntelAHCI
vboxmanage storageattach $VM_NAME --storagectl "SATA Controller" --port 0 --device 0 --type hdd --medium $VM_HD_PATH
vboxmanage storagectl $VM_NAME --name "IDE Controller" --add ide
vboxmanage storageattach $VM_NAME --storagectl "IDE Controller" --port 0 --device 0 --type dvddrive --medium $UBUNTU_ISO_PATH
vboxmanage modifyvm $VM_NAME --ioapic on
vboxmanage modifyvm $VM_NAME --memory 1024 --vram 128
vboxmanage modifyvm $VM_NAME --nic1 nat
vboxmanage modifyvm $VM_NAME --natpf1 "guestssh,tcp,,2222,,22"
vboxmanage modifyvm $VM_NAME --natdnshostresolver1 on
vboxmanage sharedfolder add $VM_NAME --name shared --hostpath $SHARED_PATH --automount
```

### Start the VM for the first time

For the first boot, we will start the VM with a graphical display so we can install
the Ubuntu operating system. **From your OS X terminal**:

```bash
vboxmanage startvm UbuntuServer
```

The VM will boot from the DVD Drive, which has the Ubuntu Server installation CD image loaded. 

### Install Ubuntu Server

Install Ubuntu Server using the installation wizard with the default settings. The installer is interactive - it should take about 10 minutes to complete the installation. As part of the installation you will be asked to select a username and a password. 

After installation is complete, the machine will reboot. Log in at the prompt.

**Hint**: If you accidentally click on the VM GUI window, VirtualBox may "hijack" your mouse pointer to try passing it to the VM. If this happens and you lose your mouse pointer, press the left command key to get your mouse pointer back.

### Install the OpenSSH Server

After installing the Ubuntu operating system and logging in to VM, to install the ssh server, issue the following command **in the Ubuntu VM**:

```bash
sudo apt-get update
sudo apt-get install -y openssh-server
```

Now you can try logging into your virtual machine over ssh through port 2222, which has been set up to forward to port 22 of your VM. **From the OS X terminal**:

```bash
ssh -p 2222 <username>@localhost
```

Congrats! :-)

For the rest of this installation guide, I recommend issuing all VM commands over ssh because the display is better than the VM GUI console, and you can easily paste commands into the Mac ssh terminal.

### Install VirtualBox Guest Additions (for shared folders)

To share a folder from your host machine (i.e. Mac) with the VM, you need to install
the VirtualBox Guest Additions in the VM. 

Before you can install the Guest additions, you need to install `gcc` and `make` into the VM. Make sure your laptop is connected to the internet (**in the VM**):

```bash
sudo apt-get -y install gcc make linux-headers-$(uname -r)
```


From the VirtualBox VM GUI window menu, select "Devices -> Insert Guest Additions CD Image...". If prompted, choose "Force Unmount". 

This will insert the VirtualBox GuestAdditions installation CD into the VM's DVD drive. From the VM terminal (or, more comfortably, the ssh terminal), mount the CD drive and run the installation script. **In the VM**:

```bash
sudo mount /dev/sr0 /media/cdrom
sudo /media/cdrom/VBoxLinuxAdditions.run
```

Finally, add your user to the `vboxsf` group so you can access shared folders (**in the VM**)

```bash
sudo usermod -g vboxsf <username>
```


For the GuestAdditions installation to take effect, you need to reboot the VM. We'll take care of that in the next section when we boot the VM without a GUI.


### Starting the VM without GUI.

Now that ssh has been installed and configured, you can run the VM in the background without a GUI window.

First, shutdown the VM using one of these methods:

- From the VM GUI, close the window and select "Send Shutdown Signal", OR
- From the VM GUI menu, select "Machine -> ACPI Shutdown" OR
- From the Mac terminal, issue `vboxmanage controlvm UbuntuServer poweroff`

Next, start the VM without a GUI from the OS X terminal:

```bash
vboxmanage startvm UbuntuServer --type headless
```

The VM will be running in the background. Give the VM a few moments to boot up, and then you can try to log in again over ssh as before from the OX X terminal: ```ssh -p 2222 <username>@localhost```.


### Access shared folders

To access your Mac home directory from the VM:

```
cd /media/sf_shared
ls -l
```

Your files should be there. If you get a "permission denied", make sure you added your user to the `vboxsf` group.



Contratulations. Now you have a local lightweight Linux environment that you can access over ssh!


## Quick Reference

To shutdown the VM:

```bash
vboxmanage controlvm UbuntuServer poweroff
```

You can also pause the VM instead of shutting it down:

```bash
vboxmanage controlvm UbuntuServer savestate
```

To start the VM:

```bash
vboxmanage startvm UbuntuServer --type headless
```

To log into the VM over ssh:

```bash
ssh -p 2222 <username>@localhost
```

## Additional Tweaks

Here are some solutions to other issues that may arise:

### Configure the Grub Boot Loader

On one occasion I powered off the VM while it was booting. The next time time I tried to start the VM without the GUI, I could not log in over ssh because, unknown to me at the time, the VM was sitting in the GRUB bootloader menu waiting for my input. 

You can configure GRUB to timeout by editing the VM's GRUB configuration file at
`/etc/default/grub` with the line:

```
GRUB_RECORDFAIL_TIMEOUT=2
```

which will
timeout the bootloader with the default selection after 2 seconds whenever the system
is started after the last boot failed. For more info, see the [Ubuntu GRUB 2 page.](https://help.ubuntu.com/community/Grub2).

### Keeping SSH Alive when laptop sleeps

Configure the VM ssh server to keep connections alive by editing the VM's config file
`/etc/ssh/sshd_config` and adding the following:

```bash
ClientAliveInterval 300
ClientAliveCountMax 2
```

When your laptop sleeps, you may find that your ssh connection to the VM is terimnated.
This is the result of some [VirtualBox bug](https://www.virtualbox.org/ticket/12441) which has since been resolved provided that you change the VM's DNS resolution setting:

```bash
VBoxManage modifyvm UbuntuServer --natdnshostresolver1 on
```

That did the trick for me.





