# 🚀 VRAI Data Analyzer - Azure Pipelines Deployment

A FastAPI-based simulation data analysis service with automated Azure deployment using Azure Pipelines.

## 📋 Overview

This project demonstrates a complete DevOps pipeline for deploying a Python FastAPI application to Azure App Service with:
- **Automated CI/CD** using Azure Pipelines
- **Azure App Service** for hosting
- **Azure Cosmos DB** for data storage
- **Application Insights** for monitoring
- **Multi-environment support** (dev/prod)

## 🏗️ Architecture

```
GitHub Repository → Azure Pipelines → Azure App Service + Cosmos DB
```

### Application Stack
- **Backend**: Python 3.12 + FastAPI
- **Database**: Azure Cosmos DB (NoSQL)
- **Hosting**: Azure App Service (Linux)
- **Monitoring**: Application Insights
- **CI/CD**: Azure Pipelines

## 🚀 Quick Start

### Prerequisites
- Azure subscription (school account supported)
- Azure DevOps account
- GitHub repository access

### Setup Steps

1. **Create Azure DevOps Project**
   - Go to [Azure DevOps](https://dev.azure.com)
   - Create new project: `VRAI-Data-Analyzer`

2. **Connect to GitHub**
   - Create new pipeline
   - Connect to this GitHub repository
   - Azure DevOps will detect `azure-pipelines.yml`

3. **Setup Service Connection**
   - Create Azure Resource Manager service connection
   - Name it exactly: `AzureServiceConnection`
   - Grant access to all pipelines

4. **Create Environments**
   - Create `dev` and `prod` environments in Azure DevOps

5. **Run Pipeline**
   - Push to `develop` branch → deploys to dev
   - Push to `main` branch → deploys to production

## 🌐 API Endpoints

After deployment, your API will be available at:

### Development
- **Base URL**: `https://vrai-analyzer-dev.azurewebsites.net`
- **Health Check**: `GET /`
- **API Docs**: `GET /docs`
- **Analysis**: `POST /analyze`

### Production
- **Base URL**: `https://vrai-analyzer-prod.azurewebsites.net`
- **Health Check**: `GET /`
- **API Docs**: `GET /docs`
- **Analysis**: `POST /analyze`

## 🧪 Testing the API

### Using Python Script
```bash
# Install requests if needed
pip install requests

# Test development environment
python test_api.py https://vrai-analyzer-dev.azurewebsites.net

# Test production environment
python test_api.py https://vrai-analyzer-prod.azurewebsites.net
```

### Using PowerShell
```powershell
# Health check
Invoke-RestMethod -Uri "https://vrai-analyzer-dev.azurewebsites.net/"

# Analysis request
$testData = @{
    trainee_id = "test-pilot"
    simulation_log = @(
        @{ timestamp = 0.0; altitude = 5000; speed = 250; event = "start" },
        @{ timestamp = 5.0; altitude = 4000; speed = 310; event = "overspeed" }
    )
} | ConvertTo-Json -Depth 3

Invoke-RestMethod -Uri "https://vrai-analyzer-dev.azurewebsites.net/analyze" `
  -Method Post -Body $testData -ContentType "application/json"
```

### Using cURL
```bash
# Health check
curl https://vrai-analyzer-dev.azurewebsites.net/

# Analysis request
curl -X POST "https://vrai-analyzer-dev.azurewebsites.net/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "trainee_id": "test-pilot",
    "simulation_log": [
      {"timestamp": 0.0, "altitude": 5000, "speed": 250, "event": "start"},
      {"timestamp": 5.0, "altitude": 4000, "speed": 310, "event": "overspeed"}
    ]
  }'
```

## 📊 Pipeline Stages

### 1. Build and Test
- Set up Python 3.12
- Install dependencies with Poetry
- Run pytest unit tests
- Generate code coverage
- Create deployment artifacts

### 2. Deploy Infrastructure
- Create Azure Resource Group
- Deploy App Service Plan and App Service
- Create Cosmos DB account and containers
- Set up Application Insights

### 3. Deploy Application
- Configure App Service settings
- Deploy FastAPI application
- Set startup commands
- Perform health checks

## 🔧 Local Development

### Setup
```bash
# Install dependencies
poetry install

# Run tests
poetry run pytest

# Start development server
poetry run uvicorn src.main:app --reload
```

### Environment Variables
Create `.env` file for local development:
```
COSMOS_DB_ENDPOINT=https://localhost:8081
COSMOS_DB_KEY=your-cosmos-emulator-key
COSMOS_DB_DATABASE_NAME=data-analyzer
COSMOS_DB_CONTAINER_NAME=analysis-results
COSMOS_DB_VERIFY_SSL=false
```

## 🌍 Environment Configuration

| Environment | Branch | App Service SKU | Cosmos DB | Monitoring |
|-------------|--------|-----------------|-----------|------------|
| Development | `develop` | B1 (Basic) | Serverless | Basic |
| Production | `main` | P1v2 (Premium) | Serverless | Advanced |

## 💰 Cost Estimation

### Development Environment (~$20/month)
- App Service B1: ~$13/month
- Cosmos DB Serverless: ~$5-15/month
- Application Insights: Free tier

### Production Environment (~$80/month)
- App Service P1v2: ~$73/month
- Cosmos DB Serverless: ~$10-25/month
- Application Insights: ~$5-10/month

## 📚 Documentation

- **[Azure Pipelines Setup](AZURE_PIPELINES_SETUP.md)**: Complete setup guide
- **[Troubleshooting](TROUBLESHOOTING.md)**: Common issues and solutions

## 🛠️ Troubleshooting

### Common Issues
1. **Service Connection Fails**: See [troubleshooting guide](TROUBLESHOOTING.md)
2. **Pipeline Permissions**: Contact IT for Azure permissions
3. **App Service Won't Start**: Check Application Insights logs
4. **Cosmos DB Connection**: Verify connection strings

### Getting Help
- Check Azure DevOps pipeline logs
- Review Application Insights telemetry
- Consult Azure Portal resource health
- See [troubleshooting documentation](TROUBLESHOOTING.md)

## 🗑️ Cleanup

To delete all Azure resources:
```bash
az group delete --name rg-vrai-analyzer --yes --no-wait
```

## 🎯 Development Workflow

1. **Feature Development**: Create branch → make changes → test locally
2. **Development Deployment**: Merge to `develop` → automatic deployment
3. **Production Release**: Merge `develop` to `main` → automatic deployment

## 📈 Monitoring

- **Application Insights**: Performance and error tracking
- **App Service Logs**: Real-time application logs
- **Cosmos DB Metrics**: Database performance monitoring
- **Pipeline History**: Deployment success tracking

## 🎉 Success Criteria

✅ Pipeline runs successfully  
✅ All tests pass  
✅ Application deploys to Azure  
✅ Health check endpoint responds  
✅ API analysis endpoint works  
✅ Data saves to Cosmos DB  
✅ Monitoring shows telemetry  

---

**Built with ❤️ for VRAI using Azure Pipelines**
