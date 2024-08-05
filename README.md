<!-- clean every thing -->
```sh
docker system prune -a
```

<!-- Test case -->
```sh
cd user-auth-service && python -m unittest discover -s tests &&
cd ../product-management-service && python -m unittest discover -s tests && 
cd ../order-processing-service && python -m unittest discover -s tests
```