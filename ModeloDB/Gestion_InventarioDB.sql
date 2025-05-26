CREATE TABLE "Proveedores" (
  "PK_ID_Proveedor" integer PRIMARY KEY,
  "Nombre" varchar,
  "Correo" varchar,
  "Teléfono" varchar
);

CREATE TABLE "Compras" (
  "PK_ID_Compras" integer PRIMARY KEY,
  "FK_ID_Proveedor" integer NOT NULL,
  "FK_ID_Trabajador" integer NOT NULL,
  "Fecha" timestamp,
  "Monto_Total" integer
);

CREATE TABLE "Productos_Comprados" (
  "FK_ID_Compras" integer NOT NULL,
  "FK_ID_Catalogo" integer NOT NULL,
  "Cantidad" integer,
  "Precio_Unidad" integer
);

CREATE TABLE "Categoria" (
  "PK_ID_Categoria" integer PRIMARY KEY,
  "Nombre" varchar
);

CREATE TABLE "Productos" (
  "PK_ID_Productos" integer PRIMARY KEY,
  "Nombre" varchar,
  "Descripcion" varchar,
  "FK_ID_Categoria" integer NOT NULL,
  "Precio_Unidad" integer,
  "Unidad_Medida" varchar,
  "Stock_Minimo" integer,
  "Stock_Actual" integer
);

CREATE TABLE "Ventas" (
  "PK_ID_Ventas" integer PRIMARY KEY,
  "FK_ID_Trabajador" integer NOT NULL,
  "Monto_Total" integer,
  "Fecha" timestamp
);

CREATE TABLE "Productos_Vendidos" (
  "FK_ID_Ventas" integer NOT NULL,
  "FK_ID_Productos" integer NOT NULL,
  "Cantidad" integer,
  "Precio_Unidad" integer
);

CREATE TABLE "Trabajadores" (
  "PK_ID_Trabajador" integer PRIMARY KEY,
  "Nombre" varchar,
  "Correo" varchar,
  "Rol" varchar
);

ALTER TABLE "Proveedores" ALTER COLUMN "PK_ID_Proveedor" ADD GENERATED ALWAYS AS IDENTITY;

ALTER TABLE "Compras" ALTER COLUMN "PK_ID_Compras" ADD GENERATED ALWAYS AS IDENTITY;

ALTER TABLE "Categoria" ALTER COLUMN "PK_ID_Categoria" ADD GENERATED ALWAYS AS IDENTITY;

ALTER TABLE "Productos" ALTER COLUMN "PK_ID_Productos" ADD GENERATED ALWAYS AS IDENTITY;

ALTER TABLE "Ventas" ALTER COLUMN "PK_ID_Ventas" ADD GENERATED ALWAYS AS IDENTITY;

ALTER TABLE "Trabajadores" ALTER COLUMN "PK_ID_Trabajador" ADD GENERATED ALWAYS AS IDENTITY;

ALTER TABLE "Compras" ADD FOREIGN KEY ("FK_ID_Proveedor") REFERENCES "Proveedores" ("PK_ID_Proveedor");

ALTER TABLE "Compras" ADD FOREIGN KEY ("FK_ID_Trabajador") REFERENCES "Trabajadores" ("PK_ID_Trabajador");

ALTER TABLE "Productos_Comprados" ADD FOREIGN KEY ("FK_ID_Compras") REFERENCES "Compras" ("PK_ID_Compras");

ALTER TABLE "Productos_Comprados" ADD FOREIGN KEY ("FK_ID_Catalogo") REFERENCES "Productos" ("PK_ID_Productos");

ALTER TABLE "Productos" ADD FOREIGN KEY ("FK_ID_Categoria") REFERENCES "Categoria" ("PK_ID_Categoria");

ALTER TABLE "Ventas" ADD FOREIGN KEY ("FK_ID_Trabajador") REFERENCES "Trabajadores" ("PK_ID_Trabajador");

ALTER TABLE "Productos_Vendidos" ADD FOREIGN KEY ("FK_ID_Ventas") REFERENCES "Ventas" ("PK_ID_Ventas");

ALTER TABLE "Productos_Vendidos" ADD FOREIGN KEY ("FK_ID_Productos") REFERENCES "Productos" ("PK_ID_Productos");

