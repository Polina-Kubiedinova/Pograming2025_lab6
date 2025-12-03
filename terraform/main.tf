terraform {
  required_version = ">= 0.13.0"
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}
provider "aws" {
  region = "eu-central-1"
}

resource "aws_security_group" "web_app" {
  name        = "web_app"
  description = "security group"

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress{
    from_port = 5000
    to_port   = 5000
    protocol  ="tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 65535
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "web_app"
  }
}

resource "aws_key_pair" "deploy_key" {
  key_name   = "deploy_key"
  public_key = file("${path.module}/../ec2_deploy_keys.pub") # Публічний ключ, який ти створила
}

resource "aws_instance" "webapp_instance" {
  ami             = "ami-0669b163befffbdfc"
  instance_type   = "t3.micro"
  vpc_security_group_ids = [aws_security_group.web_app.id]
  key_name               = aws_key_pair.deploy_key.key_name

  tags = {
    Name = "webapp_instance"
  }
}

output "instance_public_ip" {
  value     = aws_instance.webapp_instance.public_ip
  sensitive = true
}
