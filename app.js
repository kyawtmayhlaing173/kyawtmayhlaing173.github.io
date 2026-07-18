

// --- PHONE SCREEN TAB NAVIGATION ---
const tabButtons = document.querySelectorAll('.tab-item');
const appScreens = document.querySelectorAll('.app-screen');

// Map phone tabs to desktop sections for scrolling
const sectionMapping = {
  home: 'body',
  work: 'work-details',
  skills: 'credentials-details',
  projects: 'project-details',
  contact: 'contact-details'
};

tabButtons.forEach(btn => {
  btn.addEventListener('click', () => {
    const targetScreen = btn.getAttribute('data-screen');
    
    // 1. Switch active screen inside the phone viewport
    appScreens.forEach(screen => {
      screen.classList.remove('active');
      if (screen.id === `screen-${targetScreen}`) {
        screen.classList.add('active');
      }
    });
    
    // 2. Switch active tab icon highlight
    tabButtons.forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    
    // 3. Smooth-scroll desktop details pane to the mapped section
    const targetSectionId = sectionMapping[targetScreen];
    if (targetSectionId === 'body') {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    } else {
      const element = document.getElementById(targetSectionId);
      if (element) {
        element.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    }
  });
});


// --- PHONE ITEM TAP TO SCROLL & HIGHLIGHT ---
const clickableCards = document.querySelectorAll('.clickable-card');

clickableCards.forEach(card => {
  card.addEventListener('click', () => {
    const scrollToId = card.getAttribute('data-scroll-to');
    const targetElement = document.getElementById(scrollToId);
    
    if (targetElement) {
      // Scroll target element to center of screen
      targetElement.scrollIntoView({ behavior: 'smooth', block: 'center' });
      
      // Add glowing highlight effect
      targetElement.classList.add('glow-highlight');
      setTimeout(() => {
        targetElement.classList.remove('glow-highlight');
      }, 1800);
    }
  });
});


// --- SIMULATOR SKILLS ACCORDION ---
const simSkillCards = document.querySelectorAll('.sim-skill-card');

simSkillCards.forEach(card => {
  card.addEventListener('click', () => {
    // Toggle active category
    simSkillCards.forEach(c => c.classList.remove('active'));
    card.classList.add('active');
  });
});


// --- BIDIRECTIONAL SCROLL SYNCHRONIZATION ---

const detailsPane = document.querySelector('.details-pane');
const workAppContent = document.querySelector('#screen-work .app-content');
const projectsAppContent = document.querySelector('#screen-projects .app-content');

let isSyncing = false; // Flag to prevent scroll event loop feedback
let syncTimeout;

// 1. Sync: Scrolling details pane updates phone simulator tabs/screens
const syncTabsOnDetailsScroll = () => {
  if (window.innerWidth <= 992 || isSyncing) return;

  const scrollPosition = detailsPane.scrollTop + detailsPane.clientHeight / 3;
  let activeSection = 'home';
  
  const sections = [
    { id: 'work-details', key: 'work' },
    { id: 'project-details', key: 'projects' },
    { id: 'credentials-details', key: 'skills' },
    { id: 'contact-details', key: 'contact' }
  ];
  
  sections.forEach(sec => {
    const element = document.getElementById(sec.id);
    if (element) {
      const topOffset = element.offsetTop;
      if (scrollPosition >= topOffset) {
        activeSection = sec.key;
      }
    }
  });
  
  // Highlight correct tab & show corresponding simulator screen
  tabButtons.forEach(btn => {
    const screenKey = btn.getAttribute('data-screen');
    if (screenKey === activeSection) {
      if (!btn.classList.contains('active')) {
        tabButtons.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        
        appScreens.forEach(screen => {
          screen.classList.remove('active');
          if (screen.id === `screen-${screenKey}`) {
            screen.classList.add('active');
          }
        });
      }
    }
  });
};

// 2. Sync: Scrolling simulator viewport scrolls details pane to matching cards
const syncDetailsOnSimScroll = (simViewport) => {
  if (window.innerWidth <= 992 || isSyncing) return;
  
  const cards = simViewport.querySelectorAll('.clickable-card');
  const containerRect = simViewport.getBoundingClientRect();
  const containerCenter = containerRect.top + containerRect.height / 2;
  
  let closestCard = null;
  let minDistance = Infinity;
  
  // Find which card is closest to the middle of the simulator screen
  cards.forEach(card => {
    const cardRect = card.getBoundingClientRect();
    const cardCenter = cardRect.top + cardRect.height / 2;
    const distance = Math.abs(cardCenter - containerCenter);
    
    if (distance < minDistance) {
      minDistance = distance;
      closestCard = card;
    }
  });
  
  if (closestCard) {
    const scrollToId = closestCard.getAttribute('data-scroll-to');
    const targetElement = document.getElementById(scrollToId);
    if (targetElement) {
      isSyncing = true;
      targetElement.scrollIntoView({ behavior: 'smooth', block: 'center' });
      
      // Release lock after smooth scroll completes
      clearTimeout(syncTimeout);
      syncTimeout = setTimeout(() => {
        isSyncing = false;
      }, 700);
    }
  }
};

// Listeners
if (detailsPane) {
  detailsPane.addEventListener('scroll', syncTabsOnDetailsScroll);
}

if (workAppContent) {
  workAppContent.addEventListener('scroll', () => {
    syncDetailsOnSimScroll(workAppContent);
  });
}

if (projectsAppContent) {
  projectsAppContent.addEventListener('scroll', () => {
    syncDetailsOnSimScroll(projectsAppContent);
  });
}

