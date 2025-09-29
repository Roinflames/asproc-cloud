select table_name
  from user_tables;

select column_name,
       data_type,
       data_length
  from user_tab_columns;

select username
  from all_users
 order by username;

-- Lista todos los schemas y tablas accesibles
select owner as schema_name,
       table_name
  from all_tables
 order by owner,
          table_name;

-- Crear una nueva tabla
create table nueva_tabla (
   id             number primary key,
   nombre         varchar2(100),
   fecha_creacion date default sysdate
);

-- Insertar datos en la nueva tabla
insert into nueva_tabla (
   id,
   nombre
) values ( 1,
           'Ejemplo 1' );

-- Consultar datos de la nueva tabla
select *
  from nueva_tabla;

-- Eliminar una tabla
drop table nueva_tabla;