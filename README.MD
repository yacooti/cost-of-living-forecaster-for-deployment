# **Machine Learning Crash Course: Cost of Living Prediction in Nairobi**

## **Lesson II: Deploying Machine Learning Models to The Cloud**

## Prerequisites
This course requires you to have:
- Docker installed on your computer.
- A Docker Hub account. [Create one here](https://hub.docker.com/).
- A small budget of about $20 - $30 to acquire a domain name and cloud storage.
  - **Domain Name**: This will act as the web address for the outside world to access your model. You can use [this link](http://namecheap.pxf.io/c/1723848/487331/5618) to purchase a domain name from Namecheap.
  - **Cloud Storage**: This is where our model and application code will be stored, so that it can be served through our domain name. It could be DigitalOcean, AWS, GCP, MS Azure, or any other hosting provider for your app. If you don’t have this, you can use [this link](https://m.do.co/c/d8f3d87a69a0) to get free credits, which you can use to access DigitalOcean droplets for 2 months. You may be required to pay $5 using a debit or credit card.

We will learn how to purchase the domain name and cloud storage later on in this course. But for now, we will start with deploying to Docker.

## Setting Up The Project
Head over to the introductory lesson page and follow the instructions to clone and train the model:

[GitHub Repository](https://github.com/yacooti/cost-of-living-forecaster)

---

## 1. Create `docker-compose.yml`
Create a `docker-compose.yml` file in your project root:

```yaml
services:
  app:
    image: yourdockerhubusername/cost-of-living-forecaster:v1
    container_name: cost-of-living-forecaster
    ports:
      - "9000:9000"
    restart: always
```

---

## 2. Build and Push Docker Image to Docker Hub

### Create a dependencies file
Create a `requirements.txt` file in your project’s root directory, and add the following items;

```
pandas
numpy
scikit-learn
joblib
fastapi
uvicorn
xgboost
```

### (a) Create a Docker file
Create a `Dockerfile` file in your project’s root directory, and add the following code;
```
# Use official Python image
FROM python:3.10

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy project files
COPY . .


# Run FastAPI app
CMD ["uvicorn", "entrypoint:application", "--host", "0.0.0.0", "--port", "9000"]
```

### (b) Build the Image
```sh
docker build -t yourdockerhubusername/cost-of-living-forecaster:v1 .
```
### (c) Start Docker
```sh
docker compose up
```

### (d) Check that Everything Works Fine
- Go to [http://127.0.0.1:9000](http://127.0.0.1:9000)

### (e) Log in to Docker Hub From Your Terminal
```sh
docker login
```

### (f) Push the Image
```sh
docker push yourdockerhubusername/cost-of-living-forecaster:v1
```

---

## 3. Set Up a DigitalOcean Droplet

### (a) Create a Droplet
- Go to [DigitalOcean](https://cloud.digitalocean.com/)
- Click **Create Droplet**
- Choose **Ubuntu 22.04** (recommended)
- Select **Basic Plan** (Start with $5/month)
- Choose a region close to your users
- Select **SSH Key Authentication** (see next step)

### (b) Set Up SSH Keys
On your local machine, generate SSH keys (if not already done):

```sh
ssh-keygen -t rsa -b 4096 -C "your-email@example.com"
```

Add the public key to DigitalOcean:
- Copy it: `cat ~/.ssh/id_rsa.pub` or `cat ~/.ssh/id_ed25519.pub` depending on the **signature scheme** you used to generate your keys.
- Paste it into **SSH Keys** while creating the droplet.

Connect to the droplet:

```sh
ssh root@your-droplet-ip
```

### (c) Create a Sudo User


Run the following commands to create a new user `deploy` and grant it sudo privileges:

```bash
sudo adduser deploy
sudo usermod -aG sudo deploy
su - deploy
```

#### Generate SSH Key Pair on Your Local Machine

On your local computer, generate an SSH key pair if you don’t have one:

```bash
ssh-keygen -t rsa -b 4096 -C "your-email@example.com"
```

When prompted, press Enter to save the key to the default location (`~/.ssh/id_rsa`).

#### Copy the SSH Key to the Server

First, display your public key on your local machine:

```bash
cat ~/.ssh/id_rsa.pub
```

Or

```bash
cat ~/.ssh/id_ed25519.pub 
```

Then, SSH into the server as the root user:

```bash
ssh root@your-server-ip
```

Switch to the `deploy` user:

```bash
su - deploy
```

Create or edit the `authorized_keys` file:

```bash
nano ~/.ssh/authorized_keys
```

Paste the copied key into this file, save, and exit.

Then, try logging in:

```bash
ssh deploy@your-server-ip
```

If successful, you can now SSH into the server as `deploy`.

#### Set Up SSH Key for GitHub Access

On the server, generate an SSH key for GitHub:

```bash
ssh-keygen -t rsa -b 4096 -C "your-server-email@example.com"
```

Add the new key to the SSH agent:

```bash
eval "$(ssh-agent -s)"
sudo ssh-add ~/.ssh/id_rsa
```

Display the public key:

```bash
cat ~/.ssh/id_rsa.pub 
```

Or

```bash
cat ~/.ssh/id_ed25519.pub 
```

Copy and add this key to GitHub:

1. Go to GitHub > Settings > SSH and GPG keys.
2. Click **New SSH Key**.
3. Paste the key and save.

Test the connection:

```bash
ssh -T git@github.com
```

If successful, you should see a welcome message from GitHub.

#### Cloning the Project Repository

Once SSH keys are set up, clone the project:

```bash
git clone git@github.com:your-username/cost-of-living-forecaster.git
cd cost-of-living-forecaster
```

---

## 4. Install Docker and Docker Compose

Update the system and install required packages:

```sh
sudo apt update && sudo apt upgrade -y
sudo apt install -y docker.io
sudo systemctl enable --now docker
```

Install Docker Compose:

```sh
sudo curl -SL https://github.com/docker/compose/releases/latest/download/docker-compose-linux-x86_64 -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

Verify installation:

```sh
docker --version
docker-compose --version
```

---

## 5. Start Docker On the Server

Start docker in the background:

```sh
docker-compose up -d
```

Check running containers:

```sh
docker ps
```

---

## 6. Configure Namecheap DNS

1. Log in to [Namecheap](https://www.namecheap.com/).
2. Navigate to **Domain List** > **Manage** your domain.
3. Under **Advanced DNS**, add two **A Records**:
   - `@` → `your-droplet-ip`
   - `www` → `your-droplet-ip`
4. Wait for DNS propagation (can take a few minutes).

Test with:

```sh
ping yourdomain.com
```

---

## 7. Expose the App Publicly

### (a) Allow Traffic on Port 9000
```sh
sudo ufw allow 9000
sudo ufw enable
```

### (b) Set Up Nginx as a Reverse Proxy
Install Nginx:

```sh
sudo apt install nginx -y
```

Create a configuration file:

```sh
sudo nano /etc/nginx/sites-available/cost-of-living
```

Paste the following:

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:9000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable the site and restart Nginx:

```sh
sudo ln -s /etc/nginx/sites-available/cost-of-living /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### (c) Secure with SSL
#### Install Certbot Using snapd:
Install snapd

```sh
sudo apt install snapd
```

Install certbot

```sh
sudo snap install --classic certbot
```

Prepare the Certbot command

```sh
sudo ln -s /snap/bin/certbot /usr/bin/certbot
```

Generate and apply an SSL certificate:

```sh
sudo certbot --nginx
```

Certbot will automatically renew SSL certificates.

---

## 8. Final Testing
- Visit **http://yourdomain.com**.
- Your FastAPI app should be live!

For logs and troubleshooting:

```sh
docker-compose logs -f
```
---

# Getting Started with Git

## 1. Install Git
If you don’t have Git installed, follow these steps:

### **Windows**
1. Download Git from [git-scm.com](https://git-scm.com/downloads).
2. Run the installer and follow the default settings.
3. After installation, open **Git Bash** or **Command Prompt** and verify the installation:
   ```sh
   git --version
   ```

### **MacOS**
1. Open **Terminal** and install Git using Homebrew:
   ```sh
   brew install git
   ```
2. Verify the installation:
   ```sh
   git --version
   ```

### **Linux (Ubuntu/Debian)**
1. Open a terminal and install Git:
   ```sh
   sudo apt update && sudo apt install git -y
   ```
2. Verify the installation:
   ```sh
   git --version
   ```

## 2. Configure Git
Before using Git, set up your name and email globally:
```sh
git config --global user.name "Your Name"
git config --global user.email "your-email@example.com"
```
You can verify your configuration with:
```sh
git config --list
```

## 3. Generate SSH Key and Add to GitHub
1. Generate an SSH key (press Enter for the default location):
   ```sh
   ssh-keygen -t ed25519 -C "your-email@example.com"
   ```
2. Start the SSH agent:
   ```sh
   eval "$(ssh-agent -s)"
   ```
3. Add your SSH key:
   ```sh
   ssh-add ~/.ssh/id_ed25519
   ```
4. Copy the SSH key to your clipboard:
   ```sh
   cat ~/.ssh/id_ed25519.pub
   ```
5. Go to **GitHub → Settings → SSH and GPG keys → New SSH Key**.
6. Paste the copied key and save it.
7. Test the SSH connection:
   ```sh
   ssh -T git@github.com
   ```

## 4. Create a GitHub Repository
1. Go to [GitHub](https://github.com/) and log in.
2. Click **"New repository"**.
3. Enter a **Repository name** (e.g., `cost-of-living-forecaster`).
4. Choose **Public** or **Private**.
5. Click **Create repository**.
6. Copy the **SSH repository URL** (e.g., `git@github.com:your-username/cost-of-living-forecaster.git`).

## 5. Initialize Git in Your Project (If Its Not a Repository Already)
1. Open a terminal and navigate to your project folder:
   ```sh
   cd /path/to/your/project
   ```
2. Initialize Git:
   ```sh
   git init
   ```
3. Add the remote repository using SSH:
   ```sh
   git remote add origin git@github.com:your-username/cost-of-living-forecaster.git

## 6. Update Your Remote Repository In Your Project (When Its Already A Repository)

1. Update the remote repository using SSH:
   ```sh
   git remote set-url origin git@github.com:your-username/cost-of-living-forecaster.git
   ```

## 7. Connect to GitHub and Push Code
1. Verify the remote repository:
   ```sh
   git remote -v
   ```
2. Add all files to Git:
   ```sh
   git add .
   ```
3. Commit the changes:
   ```sh
   git commit -m "Initial commit"
   ```
4. Push the code to GitHub:
   ```sh
   git branch -M main
   git push -u origin main
   ```

## 8. Verify on GitHub
Go to **GitHub → Your Repository**, and you should see your code.

Happy coding! 🚀