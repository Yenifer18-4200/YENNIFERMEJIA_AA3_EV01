from fastapi import FastAPI, Request  # type: ignore[import-not-found]
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import HTMLResponse
from starlette.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.routers import products, orders  

# 1. Initialize the FastAPI application with metadata
app = FastAPI(
    title="Virtual Store API",
    description="Enterprise-grade architecture for managing inventory and customer orders",
    version="1.0.0",
)

# Static files mounting and template directory configuration
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# 2. Adding the CORS middleware configuration to allow cross-origin requests from the frontend 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allows any frontend website to access the API (for development purposes)
    allow_credentials=True,
    allow_methods=["*"], # Allows all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"], # Allows all custom headers
)

# Register the modular routers to the core application
app.include_router(products.router)
app.include_router(orders.router)


# ---------- HTML VIEWS ----------

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"request": request}
    )

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={"request": request}
    )

@app.get("/products-page", response_class=HTMLResponse)
async def products_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="products.html",  # Points to the products management template
        context={"request": request}
    )

@app.get("/orders-page", response_class=HTMLResponse)
async def orders_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="orders.html",    # Points to the orders management template
        context={"request": request}
    )

@app.get("/users-page", response_class=HTMLResponse)
async def users_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="users.html",     # Points to the user administration template
        context={"request": request}
    )

@app.get("/invoice-page", response_class=HTMLResponse)
async def invoice_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="invoice.html",   # Points to the billing/invoice details template
        context={"request": request}
    )

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="login.html",     # Points to the user authentication template
        context={"request": request}
    )