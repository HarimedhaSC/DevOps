# Jenkins CI Lab – First CI Job

## Overview

This exercise introduces **Continuous Integration (CI)** using Jenkins. Jenkins is run in a Docker container, accessed through a browser, and configured to execute a simple Freestyle job.

The job prints confirmation messages and displays the operating system used by the Jenkins build environment.

## Objectives

- Run Jenkins locally using Docker.
- Access the Jenkins web interface.
- Unlock Jenkins and complete the initial setup.
- Create a Freestyle project.
- Configure a build step using a shell script.
- Run the job and verify the build output in Console Output.

## Prerequisites

- Docker Desktop installed and running.
- A web browser.
- Basic familiarity with PowerShell and Jenkins.

## Start Jenkins

Create a persistent Docker volume for Jenkins data:

```powershell
docker volume create jenkins_home
```

Start Jenkins in a container:

```powershell
docker run -d --name jenkins --restart unless-stopped `
  -p 8080:8080 -p 50000:50000 `
  -v jenkins_home:/var/jenkins_home `
  jenkins/jenkins:lts
```

If a container named `jenkins` already exists, start it instead of creating a second container:

```powershell
docker start jenkins
```

Check the container status:

```powershell
docker ps --filter "name=jenkins"
```

## Initial Jenkins setup

1. Open [http://localhost:8080](http://localhost:8080).
2. Retrieve the initial administrator password from the container:

   ```powershell
   docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
   ```

3. Enter the password in the Jenkins setup page.
4. Install the suggested plugins and create the administrator account when prompted.
5. Finish setup and open the Jenkins dashboard.

> **Note:** Jenkins is running inside a Linux container. For this environment, use **Execute shell** in the job configuration, not **Execute Windows batch command**.

## Create the first CI job

1. From the Jenkins dashboard, select **New Item**.
2. Enter `First-CI-Job` as the item name.
3. Select **Freestyle project**, then select **OK**.
4. In the job configuration, find **Build Steps**.
5. Select **Add build step → Execute shell**.
6. Add the following script:

   ```bash
   echo "Hello from Jenkins CI!"
   echo "Build and automation test successful."
   uname -s
   ```

7. Save the job.
8. Select **Build Now**.
9. Open the build entry and select **Console Output** to review the result.

## Expected output

The console should include output similar to:

```text
Hello from Jenkins CI!
Build and automation test successful.
Linux
Finished: SUCCESS
```

The build number and surrounding Jenkins log messages may differ.

## Troubleshooting

### Error: `Cannot run program "cmd": No such file or directory`

**Cause:** The job uses **Execute Windows batch command**, which expects Windows' `cmd` executable. The Jenkins container is Linux-based.

**Fix:**

1. Open `First-CI-Job` and select **Configure**.
2. Remove the **Execute Windows batch command** build step.
3. Add **Execute shell** instead.
4. Use the Bash script shown above, save, and run the job again.

### Jenkins page does not open

- Confirm Docker Desktop is running.
- Check the container with `docker ps --filter "name=jenkins"`.
- If the container is stopped, run `docker start jenkins`.
- Check the container logs with `docker logs jenkins`.

### Port 8080 is already in use

Another application may already be using port `8080`. Stop or reconfigure the conflicting application, or choose a different host port in the Docker `-p` mapping and use that port in the browser.

## Useful commands

```powershell
# Check whether Jenkins is running
docker ps --filter "name=jenkins"

# View Jenkins logs
docker logs jenkins

# Stop Jenkins
docker stop jenkins

# Start Jenkins again
docker start jenkins

# Retrieve the initial administrator password
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

## What I learned

- How to run Jenkins locally in Docker.
- How to complete Jenkins' initial setup.
- How to configure and execute a basic Freestyle CI job.
- Why build-step commands must match the operating system of the Jenkins agent.
- How to use the build console to verify whether a job succeeded.

## Technologies used

- Jenkins
- Docker
- PowerShell
- Bash / Linux shell

## Repository note

Do not include Jenkins administrator passwords, credentials, or other secrets in this repository. Jenkins data is stored in the Docker volume `jenkins_home`, separate from this README.
