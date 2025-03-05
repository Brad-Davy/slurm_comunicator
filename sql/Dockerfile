# Use the official Microsoft SQL Server image
FROM mcr.microsoft.com/mssql/server:2022-latest

# Set environment variables required for SQL Server
ENV ACCEPT_EULA=Y
ENV SA_PASSWORD=GreenHorses?
ENV MSSQL_PID=Developer

# Expose the default SQL Server port
EXPOSE 1433

# Start SQL Server when the container runs
CMD ["/opt/mssql/bin/sqlservr"]