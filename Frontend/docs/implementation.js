{
    "technical_guidelines": {
        "version": "1.0.0",
            "scope": "React Development Standards",
                "core_paradigm": {
            "definition": "Declarative UI Library",
                "fundamental_concept": "UI as a function of state. Virtual DOM (VDOM) for efficient diffing and minimal real-DOM updates."
        }
    },
    "coding_standards": {
        "naming_conventions": {
            "components": "PascalCase",
                "events": "camelCase",
                    "attributes": "camelCase (e.g., className, htmlFor)"
        },
        "jsx_syntax": {
            "expressions": "Must be wrapped in curly braces {}",
                "structure": "Independent and reusable component-based architecture"
        }
    },
    "data_flow_architecture": {
        "props": {
            "nature": "Read-only / Immutable",
                "flow": "Unidirectional (Parent to Child)",
                    "usage": "Data and functions as callbacks"
        },
        "state_management": {
            "hook": "useState",
                "immutability_rule": "Never mutate state directly. Always use setter functions with new object/array references."
        }
    },
    "project_structure": {
        "src_organization": {
            "components/common": "Atomic UI elements (Button, Input, Icon)",
                "components/layout": "Structural components (Header, Footer, Sidebar)",
                    "hooks": "Reusable custom logic / Abstraction",
                        "pages": "Container components (Business logic, route entry points)",
                            "utils": "Generic helper/utility functions"
        },
        "responsibility_matrix": {
            "pages_containers": "Handle state, business logic, and data distribution",
                "presentation_components": "Focus on UI/UX; receive data via props; UI-only internal state",
                    "custom_hooks": "Complex logic abstraction for multi-container use"
        }
    },
    "performance_and_quality": {
        "best_practices": [
            "Single Responsibility Principle (SRP)",
            "Mandatory unique and stable keys for list rendering",
            "Clean Code and self-documenting logic"
        ],
            "memoization_strategy": {
            "component_level": "React.memo for shallow prop comparison",
                "function_level": "useCallback for stable function references",
                    "value_level": "useMemo for expensive computations"
        },
        "security": {
            "xss_prevention": "Automatic JSX sanitization",
                "restricted_features": ["Avoid dangerouslySetInnerHTML unless sanitized with external libraries"]
        }
    }
}