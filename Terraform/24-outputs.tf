output "alb_dns_name" {
  description = "The DNS name of the ALB Ingress - Paste it into DNS Alias Record in Domain Name Provider"
  value       = kubernetes_ingress_v1.app_ingress.status[0].load_balancer[0].ingress[0].hostname
}