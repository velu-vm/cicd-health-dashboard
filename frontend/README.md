# CI/CD Health Dashboard - Frontend

A modern, responsive React application for monitoring CI/CD pipeline health with real-time metrics and build tracking.

## Features

- **📊 Dashboard Overview**: Summary cards showing success rates, failure rates, build times, and status
- **📈 Metrics Visualization**: Interactive charts using Recharts for build activity over time
- **🔍 Build Management**: Sortable table of recent builds with detailed information
- **📋 Build Details**: Comprehensive view of individual builds with raw payload inspection
- **📱 Responsive Design**: Mobile-first design that works on all device sizes
- **🎨 Modern UI**: Clean, professional interface built with Tailwind CSS
- **⚡ Real-time Updates**: Live data from the backend API with refresh capabilities

## Tech Stack

- **Framework**: React 18 with TypeScript
- **Build Tool**: Vite for fast development and optimized builds
- **Styling**: Tailwind CSS with custom component classes
- **Charts**: Recharts for data visualization
- **Icons**: Lucide React for consistent iconography
- **Routing**: React Router for navigation
- **State Management**: React hooks for local state

## Quick Start

### Prerequisites

- Node.js 18+ 
- npm or yarn
- Backend API running (see backend README)

### Installation

1. **Install dependencies**
   ```bash
   npm install
   ```

2. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your API configuration
   ```

3. **Start development server**
   ```bash
   npm run dev
   ```

4. **Open in browser**
   Navigate to `http://localhost:5173`

## Environment Configuration

| Variable | Description | Default |
|----------|-------------|---------|
| `VITE_API_BASE` | Backend API base URL | `http://localhost:8000` |
| `VITE_DEBUG` | Enable debug mode | `false` |

## Project Structure

```
src/
├── components/          # Reusable UI components
│   ├── SummaryCards.tsx    # Dashboard summary metrics
│   ├── MetricsChart.tsx    # Build activity charts
│   ├── BuildsTable.tsx     # Builds list with sorting
│   └── BuildLogDrawer.tsx  # Build details drawer
├── pages/              # Page components
│   ├── Dashboard.tsx       # Main dashboard view
│   └── BuildDetails.tsx    # Individual build details
├── services/           # API and external services
│   └── api.ts             # Backend API client
├── App.tsx            # Main app with routing
└── index.css          # Global styles and Tailwind
```

## Components

### SummaryCards
Displays key metrics in an attractive card layout:
- Success Rate with trending indicator
- Failure Rate with trending indicator  
- Average Build Time with clock icon
- Last Build Status with status-specific styling

### MetricsChart
Interactive bar chart showing build activity over the last 7 days:
- Success vs Failure counts per day
- Responsive design with custom tooltips
- Mock data generation when API is unavailable
- Built with Recharts for smooth interactions

### BuildsTable
Sortable table of recent builds with:
- Status chips with color coding
- Sortable columns (status, provider, branch, duration, started_at)
- Click handlers for build details
- External links to GitHub Actions
- Responsive design with horizontal scrolling

### BuildLogDrawer
Slide-out drawer for build details:
- Comprehensive build information
- Raw payload JSON viewer
- External GitHub Actions links
- Responsive layout for mobile and desktop

## Pages

### Dashboard (/)
Main application view featuring:
- Header with navigation and refresh controls
- Summary cards for quick metrics overview
- Metrics chart for trend analysis
- Recent builds table with click-to-view functionality
- Responsive grid layout

### Build Details (/build/:id)
Detailed view of individual builds:
- Complete build information display
- Raw payload inspection
- Navigation back to dashboard
- External GitHub Actions integration

## Styling

### Tailwind CSS Classes
The application uses custom Tailwind component classes:

```css
.btn          /* Base button styles */
.btn-primary  /* Primary button variant */
.btn-secondary /* Secondary button variant */
.card         /* Card container styles */
.status-chip  /* Status indicator styles */
```

### Color Scheme
- **Primary**: Blue tones for main actions and branding
- **Success**: Green for successful builds and positive metrics
- **Danger**: Red for failed builds and errors
- **Warning**: Yellow for running builds and alerts
- **Neutral**: Gray tones for text and backgrounds

## Development

### Available Scripts

```bash
npm run dev          # Start development server
npm run build        # Build for production
npm run preview      # Preview production build
npm run lint         # Run ESLint
```

### Code Organization
- **Components**: Reusable UI elements with TypeScript interfaces
- **Pages**: Route-specific components with business logic
- **Services**: API communication and external integrations
- **Types**: Shared TypeScript interfaces and types

### State Management
- **Local State**: React hooks for component-specific state
- **API State**: Loading, error, and data states managed per component
- **Navigation**: React Router for page routing and navigation

## Responsive Design

The application is built with a mobile-first approach:

- **Mobile**: Single column layout with stacked components
- **Tablet**: Two-column grid for better space utilization
- **Desktop**: Full three-column layout with sidebar navigation

### Breakpoints
- `sm`: 640px and up
- `md`: 768px and up  
- `lg`: 1024px and up
- `xl`: 1280px and up

## Performance

### Optimization Features
- **Lazy Loading**: Components load only when needed
- **Memoization**: React.memo for expensive components
- **Efficient Rendering**: Optimized re-renders with proper dependencies
- **Bundle Splitting**: Vite handles code splitting automatically

### Loading States
- Skeleton loaders for content areas
- Spinner indicators for actions
- Graceful fallbacks for missing data

## Testing

### Component Testing
Components are designed to be easily testable:
- Clear prop interfaces
- Separated business logic
- Mockable dependencies
- Accessible markup

### API Testing
The API service can be tested independently:
- Mock responses for development
- Error handling scenarios
- Network failure handling

## Deployment

### Build Process
```bash
npm run build
```

### Output
The build process creates:
- Optimized JavaScript bundles
- Minified CSS with Tailwind
- Static assets for production
- Service worker for offline support

### Environment Variables
Ensure production environment variables are set:
- `VITE_API_BASE`: Production API URL
- `VITE_DEBUG`: Set to false for production

## Contributing

### Development Workflow
1. Create feature branch
2. Implement changes with TypeScript
3. Test responsive design
4. Update documentation
5. Submit pull request

### Code Standards
- TypeScript for type safety
- Tailwind CSS for styling
- Component-based architecture
- Responsive design principles
- Accessibility best practices

## Troubleshooting

### Common Issues

**API Connection Errors**
- Verify `VITE_API_BASE` is correct
- Check backend is running
- Review network connectivity

**Build Failures**
- Clear node_modules and reinstall
- Check Node.js version compatibility
- Verify all dependencies are installed

**Styling Issues**
- Ensure Tailwind CSS is properly configured
- Check PostCSS configuration
- Verify CSS imports are correct

## Support

For issues and questions:
- Check the backend README for API documentation
- Review component documentation in code comments
- Test with the provided sample data
- Verify environment configuration

---

Built with ❤️ using React, TypeScript, and Tailwind CSS
