-- Create the database
CREATE DATABASE EmployeeCompDB;
GO

-- Switch to the new database

USE [EmployeeCompDB]
GO

/****** Object:  Table [dbo].[Employees]    Script Date: 17-05-2025 22:10:09 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[Employees](
	[EmployeeID] [int] IDENTITY(1,1) NOT NULL,
	[Name] [varchar](100) NULL,
	[Role] [varchar](50) NULL,
	[Location] [varchar](50) NULL,
	[ExperienceYears] [float] NULL,
	[Compensation] [decimal](18, 2) NULL,
	[Status] [varchar](10) NULL,
	[LastWorkingDay] [date] NULL,
PRIMARY KEY CLUSTERED 
(
	[EmployeeID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO