# 🚀 Azure Pipelines Setup Guide for VRAI Data Analyzer

## � Quick Fix for Service Connection Error

**If you see this error:**
```
Job DeployInfra: Step deployInfra input azureSubscription references service connection Azure Service Connection which could not be found.
```

**Solution:**
1. **Create the service connection first** (see Step 3 below)
2. **Name it exactly**: `AzureServiceConnection` (no spaces)
3. **Grant pipeline access** when creating the connection
4. If you use a different name, update the `azureServiceConnection` variable in `azure-pipelines.yml`

---

## �📋 Overview

This guide will help you set up Azure Pipelines to automatically build, test, and deploy your FastAPI application to Azure App Service whenever you push code to your repository.

## 🏗️ What Gets Created

The pipeline will automatically create and manage:

| Azure Resource | Name Pattern | Purpose |
|----------------|--------------|---------|
| **Resource Group** | `rg-vrai-analyzer` | Container for all resources |
| **App Service Plan** | `vrai-analyzer-{env}-plan` | Hosting infrastructure |
| **App Service** | `vrai-analyzer-{env}` | Web application hosting |
| **Cosmos DB Account** | `vrai-cosmos-{env}` | NoSQL database |
| **Cosmos DB Database** | `data-analyzer` | Application database |
| **Cosmos DB Container** | `analysis-results` | Data storage |
| **Application Insights** | `vrai-analyzer-{env}-insights` | Performance monitoring |

**Environment Mapping:**
- `main` branch → `prod` environment (P1v2 App Service)
- `develop` branch → `dev` environment (B1 App Service)

## 🔧 Setup Steps

### Step 1: Create Azure DevOps Project

1. Go to [Azure DevOps](https://dev.azure.com)
2. Sign in with your school Azure account
3. Create a new project:
   - **Name**: `VRAI-Data-Analyzer`
   - **Visibility**: Private
   - **Version control**: Git

### Step 2: Connect to GitHub Repository

1. In your Azure DevOps project, go to **Pipelines**
2. Click **Create Pipeline**
3. Select **GitHub** as your code location
4. Authorize Azure Pipelines to access your GitHub account
5. Select your repository: `gnanas1295/data-analyzer-poc`
6. Azure DevOps will detect the `azure-pipelines.yml` file

### Step 3: Create Azure Service Connection

**IMPORTANT**: This is the most critical step. The pipeline cannot run without a proper service connection.

1. In Azure DevOps, go to **Project Settings** (bottom left corner)
2. Under **Pipelines**, click **Service connections**
3. Click **+ Create service connection**
4. Select **Azure Resource Manager**
5. Choose **Service principal (automatic)** (preferred for school accounts)

**For Service Principal (Automatic):**
6. Configure the connection:
   - **Scope level**: **Subscription**
   - **Subscription**: Select your school Azure subscription
   - **Resource group**: **Leave empty** (pipeline will create it)
   - **Service connection name**: **`AzureServiceConnection`** (exactly this name)
   - **Description**: `Service connection for VRAI Data Analyzer`
   - **Grant access permission to all pipelines**: ✅ **Check this box**
7. Click **Save**

**If Automatic Fails (Common in School Accounts):**

**Option A: Service Principal (Manual) - Contact IT**
1. Contact your IT administrator and request:
   ```
   Service Principal Details Needed:
   - Application (client) ID
   - Client secret (password)
   - Tenant ID
   - Subscription ID
   ```
2. Choose **Service principal (manual)**
3. Enter the details provided by IT
4. Name it exactly: **`AzureServiceConnection`**

**Option B: Managed Identity (If Available)**
1. Choose **Managed Identity**
2. Select your subscription
3. Name it exactly: **`AzureServiceConnection`**

**⚠️ TROUBLESHOOTING:**
- **Error "Insufficient privileges"**: Contact IT for permissions
- **Error "Service principal creation failed"**: Use manual option above
- **Can't see your subscription**: Verify you're logged in with correct account

**✅ Verification:**
After creating the service connection:
1. Click on it to verify it shows "Ready to use"
2. Test the connection by clicking **Verify**
3. Ensure the name is exactly **`AzureServiceConnection`** (no spaces!)

### Step 4: Create Pipeline Environments

1. In Azure DevOps, go to **Pipelines** → **Environments**
2. Create two environments:
   
   **Environment 1:**
   - **Name**: `dev`
   - **Description**: Development environment
   
   **Environment 2:**
   - **Name**: `prod`
   - **Description**: Production environment

3. For each environment, you can optionally set up:
   - **Approvals**: Require approval before deployment
   - **Checks**: Add security validations

### Step 5: Configure Pipeline Variables (Optional)

1. Go to **Pipelines** → **Library**
2. Create a variable group called `VRAI-Config`:
   - `resourceGroup`: `rg-vrai-analyzer`
   - `location`: `East US`
   - `pythonVersion`: `3.12`

### Step 6: Update Service Connection Name (If Different)

If you created a service connection with a different name:

1. Open `azure-pipelines.yml` in your repository
2. Find this line:
   ```yaml
   - name: azureServiceConnection
     value: 'AzureServiceConnection'  # Update this to match your service connection name
   ```
3. Change `'AzureServiceConnection'` to your actual service connection name
4. Commit and push the change

**Common Service Connection Names:**
- `AzureServiceConnection` (recommended)
- `Azure-Service-Connection`
- `MyAzureConnection`
- Your subscription name

## 🚀 Running the Pipeline

### Automatic Triggers

The pipeline runs automatically when you:
- Push to `main` branch (deploys to production)
- Push to `develop` branch (deploys to development)
- Create a pull request (runs tests only)

### Manual Triggers

1. Go to **Pipelines** in Azure DevOps
2. Select your pipeline
3. Click **Run pipeline**
4. Choose the branch to deploy

## 📊 Pipeline Stages

### Stage 1: Build and Test
- ✅ Checkout source code
- ✅ Set up Python 3.12
- ✅ Install Poetry and dependencies
- ✅ Run pytest unit tests
- ✅ Generate code coverage reports
- ✅ Create deployment artifacts

### Stage 2: Deploy Infrastructure
- ✅ Create Azure resource group
- ✅ Deploy App Service Plan and App Service
- ✅ Create Cosmos DB account, database, and container
- ✅ Set up Application Insights monitoring

### Stage 3: Deploy Application
- ✅ Configure App Service settings
- ✅ Deploy FastAPI application code
- ✅ Set startup command
- ✅ Perform health checks
- ✅ Verify API endpoints

## 🌐 Application URLs

After successful deployment:

**Development Environment:**
- **API Base**: `https://vrai-analyzer-dev.azurewebsites.net`
- **Health Check**: `https://vrai-analyzer-dev.azurewebsites.net/`
- **API Docs**: `https://vrai-analyzer-dev.azurewebsites.net/docs`
- **Analysis**: `https://vrai-analyzer-dev.azurewebsites.net/analyze`

**Production Environment:**
- **API Base**: `https://vrai-analyzer-prod.azurewebsites.net`
- **Health Check**: `https://vrai-analyzer-prod.azurewebsites.net/`
- **API Docs**: `https://vrai-analyzer-prod.azurewebsites.net/docs`
- **Analysis**: `https://vrai-analyzer-prod.azurewebsites.net/analyze`

## 🧪 Testing Your API

### PowerShell Test Script
```powershell
# Test development environment
$devUrl = "https://vrai-analyzer-dev.azurewebsites.net"
$testData = @{
    trainee_id = "test-pilot-$(Get-Date -Format 'yyyyMMdd-HHmmss')"
    simulation_log = @(
        @{ timestamp = 0.0; altitude = 5000; speed = 250; event = "start" },
        @{ timestamp = 2.5; altitude = 4500; speed = 280; event = "turbulence" },
        @{ timestamp = 5.0; altitude = 4000; speed = 310; event = "overspeed" }
    )
} | ConvertTo-Json -Depth 3

# Health check
Write-Host "Health Check:" -ForegroundColor Green
Invoke-RestMethod -Uri "$devUrl/" -Method Get

# API test
Write-Host "API Test:" -ForegroundColor Green
Invoke-RestMethod -Uri "$devUrl/analyze" -Method Post -Body $testData -ContentType "application/json"
```

## 📊 Monitoring and Troubleshooting

### Azure Portal Monitoring
1. **App Service Logs**: Azure Portal → App Service → Monitoring → Log stream
2. **Application Insights**: Azure Portal → Application Insights → Live Metrics
3. **Cosmos DB Metrics**: Azure Portal → Cosmos DB → Monitoring → Metrics

### Azure DevOps Monitoring
1. **Pipeline Runs**: Pipelines → Recent runs
2. **Test Results**: Pipeline run → Tests tab
3. **Deployment History**: Pipelines → Environments → Deployment history

### Common Issues

| Issue | Symptom | Solution |
|-------|---------|----------|
| **Service Connection Fails** | Pipeline can't access Azure | Check service principal permissions |
| **App Service Won't Start** | Health check fails | Check Application Insights for startup errors |
| **Cosmos DB Connection** | API errors | Verify connection string in App Settings |
| **Build Failures** | Pipeline fails in build stage | Check test results and dependency issues |

## 💰 Cost Information

### Development Environment (~$20/month)
- **App Service B1**: ~$13/month
- **Cosmos DB Serverless**: ~$5-15/month (usage-based)
- **Application Insights**: Free tier

### Production Environment (~$80/month)
- **App Service P1v2**: ~$73/month
- **Cosmos DB Serverless**: ~$10-25/month (usage-based)
- **Application Insights**: ~$5-10/month

## 🗑️ Cleanup

To delete all resources:

1. **Via Azure Portal**:
   - Go to Resource Groups
   - Delete `rg-vrai-analyzer`

2. **Via Azure CLI**:
   ```bash
   az group delete --name rg-vrai-analyzer --yes --no-wait
   ```

## 🎯 Development Workflow

### Feature Development
```bash
# Create feature branch
git checkout -b feature/new-feature

# Make changes and commit
git add .
git commit -m "Add new feature"
git push origin feature/new-feature

# Create pull request to develop
# Pipeline runs tests automatically
```

### Development Deployment
```bash
# Merge to develop branch
git checkout develop
git merge feature/new-feature
git push origin develop

# Pipeline automatically deploys to dev environment
```

### Production Release
```bash
# Merge to main branch
git checkout main
git merge develop
git push origin main

# Pipeline automatically deploys to production environment
```

## ✅ Success Checklist

After pipeline completion, verify:

- [ ] Pipeline completed successfully in Azure DevOps
- [ ] All Azure resources created in Azure Portal
- [ ] Health check endpoint responds: `GET /`
- [ ] API documentation accessible: `GET /docs`
- [ ] Analysis endpoint works: `POST /analyze`
- [ ] Application Insights showing telemetry
- [ ] No errors in App Service logs

**🎉 Congratulations! Your FastAPI application is now automatically deployed with Azure Pipelines!**
