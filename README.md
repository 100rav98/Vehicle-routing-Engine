#Multi-Depot Vehicle Routing Optimizer


An end-to-end Operations Research application that optimizes last-mile delivery routes across multiple distribution centers while considering vehicle capacity, customer demand, service constraints, and transportation cost.

The project translates a real-world supply chain routing problem into a mathematical optimization model and exposes the solution through an interactive Streamlit decision-support application.

---

##Business Problem

Distribution networks often operate with:

- Multiple warehouses / distribution centers
- Multiple delivery vehicles
- Customers with different demand requirements
- Limited vehicle capacity
- Delivery service constraints
- Transportation costs
- Competing trade-offs between fleet utilization, distance, and service levels

A common planning question is:

> **How should customers be assigned to vehicles and depots, and in what sequence should they be visited, to minimize transportation cost while satisfying operational constraints?**

This project addresses that problem using **Operations Research and mathematical optimization**.

---

#Project Objective

The optimizer determines:

1. Which vehicle should serve each customer
2. Which depot each vehicle should operate from
3. The sequence in which customers should be visited
4. How vehicle capacity should be utilized
5. The total transportation distance/cost
6. Whether all operational constraints are satisfied

##Primary objective

Minimize total transportation distance/cost while maintaining a feasible delivery plan.

Conceptually:

```text
Minimize:

Total Transportation Cost
        ↓
while satisfying
        ↓
Customer Demand
Vehicle Capacity
Depot/Fleet Constraints
Service Constraints
Route Feasibility


Concepts Used in this project:

Graph theory
Network optimization
Traveling Salesman Problem (TSP)
Capacitated Vehicle Routing Problem (CVRP)
Multi-Depot Vehicle Routing Problem (MDVRP)
Mixed-integer optimization concepts
Objective functions
Decision variables
Constraints
Feasible vs. optimal solutions
Heuristic / baseline optimization
Scenario analysis
Sensitivity analysis
Supply chain network decision-making

Solution Architecture below :

                  ┌──────────────────────┐
                  │   Depot Information  │
                  └──────────┬───────────┘
                             │
                             ▼
                  ┌──────────────────────┐
                  │ Customer Demand Data │
                  └──────────┬───────────┘
                             │
                             ▼
                  ┌──────────────────────┐
                  │ Data Validation      │
                  └──────────┬───────────┘
                             │
                             ▼
                  ┌──────────────────────┐
                  │ Distance Matrix      │
                  └──────────┬───────────┘
                             │
                             ▼
                  ┌──────────────────────┐
                  │ OR-Tools Optimization│
                  │      Model           │
                  └──────────┬───────────┘
                             │
                             ▼
                  ┌──────────────────────┐
                  │ Optimized Routes     │
                  └──────────┬───────────┘
                             │
              ┌──────────────┼──────────────┐
              ▼              ▼              ▼
        ┌──────────┐   ┌────────────┐  ┌───────────┐
        │   KPIs   │   │ Route Map  │  │ Scenarios │
        └──────────┘   └────────────┘  └───────────┘
              │              │              │
              └──────────────┼──────────────┘
                             ▼
                  ┌──────────────────────┐
                  │ Streamlit Dashboard  │
                  └──────────────────────┘

Tech stack used:

| Area                     | Technology      |
| ------------------------ | --------------- |
| Programming              | Python          |
| Optimization             | Google OR-Tools |
| Data Processing          | Pandas          |
| Numerical Analysis       | NumPy           |
| Graph / Network Analysis | NetworkX        |
| Visualization            | Plotly          |
| Route Mapping            | Folium          |
| Web Application          | Streamlit       |
| Testing                  | Pytest          |
| Version Control          | Git             |
| Repository               | GitHub          |

The method to build the project is below : 
1. Get the data
        ↓
2. Parse the data       
        ↓
3. Validate the data
        ↓
4. Understand the data
        ↓
5. Calculate distances
        ↓
6. Build baseline solution
        ↓
7. Build optimization model
        ↓
8. Add constraints
        ↓
9. Improve solver
        ↓
10. Benchmark against Cordeau
        ↓
11. Visualization
        ↓
12. Streamlit application
        ↓
13. GitHub portfolio
