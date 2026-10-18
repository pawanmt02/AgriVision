export type SupportedLanguage = "en" | "kn" | "hi" | "es" | "sw" | "fr";

export interface TranslationDictionary {
  brand: {
    title: string;
    tagline: string;
    subtitle: string;
    universalCore: string;
    online: string;
    connecting: string;
    coreActive: string;
    deepCnnActive: string;
  };
  nav: {
    scan: string;
    map: string;
    history: string;
    analytics: string;
  };
  scanner: {
    targetCrop: string;
    autoDetect: string;
    gpsCoordinates: string;
    gpsAcquired: string;
    awaitingGps: string;
    multiModalCore: string;
    multiModalSub: string;
    readyTitle: string;
    readyDesc: string;
    openCamera: string;
    uploadImage: string;
    retake: string;
    changeImage: string;
    runDiagnostic: string;
    telemetryTitle: string;
    telemetrySla: string;
    telemetry: string[];
    galleryTitle: string;
    gallerySub: string;
    plantBadge: string;
    animalBadge: string;
  };
  diagnostic: {
    veterinaryAlertTitle: string;
    veterinaryWarningDesc: string;
    invalidImageTitle: string;
    invalidImageDesc: string;
    wrongPhotoTitle: string;
    wrongPhotoDesc: string;
    wrongPhotoBadge: string;
    retakeCorrectLeaf: string;
    cnnDomainClassification: string;
    certainty: string;
    severityTitle: string;
    surfaceArea: string;
    observedSymptoms: string;
    morphologyValidated: string;
    vetValidated: string;
    pathwaysTitle: string;
    pathwaysSub: string;
    organicTab: string;
    chemicalTab: string;
    vetOrganicTab: string;
    vetChemicalTab: string;
    biologicalProtocol: string;
    chemicalProtocol: string;
    vetHerbalProtocol: string;
    vetMedicalProtocol: string;
    prepMethod: string;
    scheduleInterval: string;
    culturalPractices: string;
    activeMolecule: string;
    applicationRate: string;
    phiDays: string;
    mandatoryPhi: string;
    safetyPrecautions: string;
    locateMap: string;
    scanAnother: string;
    listenAloud: string;
    stopSpeech: string;
    copyRx: string;
    copied: string;
    cnnBadge: string;
  };
  map: {
    title: string;
    postGisBadge: string;
    subtitle: string;
    allCrops: string;
    allSeverities: string;
    severeOnly: string;
    moderate: string;
    lowHealthy: string;
    myLocation: string;
    severeHotspots: string;
    totalClusters: string;
    activeList: string;
    liveFeed: string;
    distanceAway: string;
    certainty: string;
  };
  history: {
    title: string;
    totalRecords: string;
    subtitle: string;
    searchPlaceholder: string;
    exportLog: string;
    noScansTitle: string;
    noScansDesc: string;
    organicRx: string;
    chemicalProtocol: string;
  };
  analytics: {
    title: string;
    badge: string;
    subtitle: string;
    totalScans: string;
    severeRisk: string;
    sla: string;
    cropsMonitored: string;
    topCropsTitle: string;
    pathogenDistribution: string;
    fungal: string;
    bacterial: string;
    viral: string;
    pests: string;
    realtimeCloud: string;
    analyzedAcreage: string;
    subsecondEdge: string;
    stapleGrains: string;
    frequency: string;
    globalRatio: string;
    scansCount: string;
  };
  footer: {
    tagline: string;
    fastapi: string;
    groq: string;
    postgis: string;
  };
}

export const TRANSLATIONS: Record<SupportedLanguage, TranslationDictionary> = {
  // 1. KANNADA (ಕನ್ನಡ)
  kn: {
    brand: {
      title: "ಅಗ್ರಿವಿಷನ್ AI",
      tagline: "ಸಮಗ್ರ ಬೆಳೆ ರೋಗನಿರ್ಣಯ ಮತ್ತು ಕೃಷಿ ವಿಜ್ಞಾನ ಎಂಜಿನ್",
      subtitle: "ಕೃತಕ ಬುದ್ಧಿಮತ್ತೆ ಮತ್ತು ಡೀಪ್-ಸಿಎನ್‌ಎನ್ ಆಧಾರಿತ ರೋಗ ಪತ್ತೆ",
      universalCore: "ಸಾರ್ವತ್ರಿಕ ಕೋರ್",
      online: "ಆನ್‌ಲೈನ್",
      connecting: "ಸಂಪರ್ಕಿಸುತ್ತಿದೆ",
      coreActive: "ಕೋರ್ ಸಕ್ರಿಯ",
      deepCnnActive: "ಡೀಪ್ CNN ಸಕ್ರಿಯ"
    },
    nav: {
      scan: "ಸ್ಕ್ಯಾನ್ ಮತ್ತು ರೋಗನಿರ್ಣಯ",
      map: "ರೋಗ ಹರಡುವಿಕೆ ನಕ್ಷೆ (GIS)",
      history: "ಕ್ಷೇತ್ರ ಲಾಗ್‌ಗಳು",
      analytics: "ವಿಶ್ಲೇಷಣೆ"
    },
    scanner: {
      targetCrop: "ಗುರಿ ಬೆಳೆ / ಜಾನುವಾರು",
      autoDetect: "ಸ್ವಯಂ ಪತ್ತೆ (ಬೆಳೆ ಮತ್ತು ಜಾನುವಾರು)",
      gpsCoordinates: "ಕ್ಷೇತ್ರದ ಜಿಪಿಎಸ್ ನಿರ್ದೇಶಾಂಕಗಳು",
      gpsAcquired: "ಜಿಪಿಎಸ್ ಪಡೆಯಲಾಗಿದೆ",
      awaitingGps: "ಉಪಗ್ರಹ ಸಿಗ್ನಲ್‌ಗಾಗಿ ಕಾಯಲಾಗುತ್ತಿದೆ...",
      multiModalCore: "ಮಲ್ಟಿ-ಮೋಡಲ್ + ಡೀಪ್ CNN ಕೋರ್",
      multiModalSub: "PyTorch CNN + ಅಗ್ರಾನಮಿ ಎಂಜಿನ್",
      readyTitle: "ಬೆಳೆ ರೋಗ ತಪಾಸಣೆಗೆ ಸಿದ್ಧವಾಗಿದೆ",
      readyDesc: "ಬಾಧಿತ ಎಲೆ ಅಥವಾ ರೋಗಲಕ್ಷಣದ ಮೇಲೆ ಕ್ಯಾಮೆರಾ ಇರಿಸಿ, ಫೋಟೋ ಅಪ್‌ಲೋಡ್ ಮಾಡಿ ಅಥವಾ ಮಾದರಿಯನ್ನು ಆಯ್ಕೆಮಾಡಿ.",
      openCamera: "ಕ್ಯಾಮೆರಾ ತೆರೆಯಿರಿ",
      uploadImage: "ಚಿತ್ರ ಅಪ್‌ಲೋಡ್ ಮಾಡಿ",
      retake: "ಮತ್ತೆ ತೆಗೆಯಿರಿ",
      changeImage: "ಚಿತ್ರ ಬದಲಾಯಿಸಿ",
      runDiagnostic: "ರೋಗನಿರ್ಣಯ ಎಂಜಿನ್ ಚಾಲನೆ",
      telemetryTitle: "ಎಲೆಯ ಅಂಗಾಂಶ ಸ್ಕ್ಯಾನಿಂಗ್...",
      telemetrySla: "ವಿಷನ್ ಪೈಪ್‌ಲೈನ್ • ವೇಗ < ೨೦೦ ಮಿ.ಸೆಕೆಂಡ್",
      telemetry: [
        "ಹೆಚ್ಚಿನ ರೆಸಲ್ಯೂಶನ್ ಪಿಕ್ಸೆಲ್‌ಗಳನ್ನು ಪಡೆಯಲಾಗುತ್ತಿದೆ...",
        "ಪೈಟಾರ್ಚ್ ಡೀಪ್-ಸಿಎನ್‌ಎನ್ (CNN) ಪ್ರಕ್ರಿಯೆ ಚಾಲನೆಯಲ್ಲಿದೆ...",
        "ಎಲೆಗಳ ಹಸಿರು ಹಾಗೂ ಕ್ಲೋರೋಫಿಲ್ ಕೊಳೆತ ವಿಶ್ಲೇಷಣೆ...",
        "ರೋಗಪೀಡಿತ ಗಾಯಗಳ ಅಂಚುಗಳನ್ನು ಸ್ಕ್ಯಾನ್ ಮಾಡಲಾಗುತ್ತಿದೆ...",
        "ಜೈವಿಕ ಮತ್ತು ರಾಸಾಯನಿಕ ಪರಿಹಾರ ಕ್ರಮಗಳನ್ನು ಸಿದ್ಧಪಡಿಸಲಾಗುತ್ತಿದೆ..."
      ],
      galleryTitle: "ತತ್ಕ್ಷಣದ ಪರಿಶೀಲನಾ ಮಾದರಿ ಗ್ಯಾಲರಿ",
      gallerySub: "AI ಮಾದರಿಯನ್ನು ತಕ್ಷಣವೇ ಪರೀಕ್ಷಿಸಲು ಮಾದರಿಯನ್ನು ಆರಿಸಿ",
      plantBadge: "ಬೆಳೆ",
      animalBadge: "ಪ್ರಾಣಿ"
    },
    diagnostic: {
      veterinaryAlertTitle: "ಪಶು ವೈದ್ಯಕೀಯ ತುರ್ತು ಎಚ್ಚರಿಕೆ",
      veterinaryWarningDesc: "ಇದು ಪ್ರಾಣಿ/ಜಾನುವಾರುಗಳ ರೋಗವಾಗಿದೆ. ಯಾವುದೇ ಕಾರಣಕ್ಕೂ ಬೆಳೆಗಳಿಗೆ ಬಳಸುವ ಕೀಟನಾಶಕ ಅಥವಾ ಶಿಲೀಂಧ್ರನಾಶಕಗಳನ್ನು ಪ್ರಾಣಿಗಳಿಗೆ ಹಾಕಬೇಡಿ. ತಕ್ಷಣವೇ ಪಶು ವೈದ್ಯರನ್ನು ಸಂಪರ್ಕಿಸಿ.",
      invalidImageTitle: "ಕೃಷಿ ವಿಷಯ ಪತ್ತೆಯಾಗಿಲ್ಲ",
      invalidImageDesc: "ಚಿತ್ರದಲ್ಲಿ ಯಾವುದೇ ಬೆಳೆಯ ಎಲೆ ಅಥವಾ ಪ್ರಾಣಿ ರೋಗದ ಲಕ್ಷಣಗಳು ಕಂಡುಬಂದಿಲ್ಲ. ದಯವಿಟ್ಟು ಸ್ಪಷ್ಟ ಫೋಟೋ ತೆಗೆದುಕೊಳ್ಳಿ.",
      wrongPhotoTitle: "ದೋಷ: ಇದು ಸಸ್ಯ ರೋಗದ ಫೋಟೋ ಅಲ್ಲ",
      wrongPhotoDesc: "ಅಪ್‌ಲೋಡ್ ಮಾಡಲಾದ ಚಿತ್ರವು ಸಸ್ಯ ಅಥವಾ ಬೆಳೆ ರೋಗದ ಎಲೆಯಲ್ಲ (ಮಾನವ, ಪ್ರಾಣಿ, ವಾಹನ, ವಸ್ತು ಅಥವಾ ಕೃಷಿಯೇತರ ವಿಷಯ). ಅಗ್ರಿವಿಷನ್ ಕೇವಲ ಸಸ್ಯಗಳ ಎಲೆ ರೋಗನಿರ್ಣಯ ಎಂಜಿನ್ ಆಗಿದೆ. ದಯವಿಟ್ಟು ಬಾಧಿತ ಬೆಳೆಯ ಎಲೆಯ ಸ್ಪಷ್ಟ ಫೋಟೋ ಅಪ್‌ಲೋಡ್ ಮಾಡಿ.",
      wrongPhotoBadge: "ದೋಷ: ತಪ್ಪಾದ ಫೋಟೋ (ಸಸ್ಯದ ಎಲೆಯಲ್ಲ)",
      retakeCorrectLeaf: "ಸಸ್ಯದ ಎಲೆಯ ಫೋಟೋ ಅಪ್‌ಲೋಡ್ ಮಾಡಿ",
      cnnDomainClassification: "ಸಿಎನ್‌ಎನ್ ಡೊಮೇನ್ ವರ್ಗೀಕರಣ",
      certainty: "ಮಾದರಿ ನಿಖರತೆ",
      severityTitle: "ಸೋಂಕಿನ ತೀವ್ರತೆ",
      surfaceArea: "ಬಾಧಿತ ಮೇಲ್ಮೈ ವಿಸ್ತೀರ್ಣ",
      observedSymptoms: "ಕಂಡುಬಂದ ರೋಗಲಕ್ಷಣಗಳು",
      morphologyValidated: "ಎಲೆಯ ರಚನೆ ದೃಢೀಕರಿಸಲಾಗಿದೆ",
      vetValidated: "ಪಶು ರೋಗ ದೃಢೀಕರಿಸಲಾಗಿದೆ",
      pathwaysTitle: "ಕಾರ್ಯಸಾಧ್ಯ ಕೃಷಿ ಚಿಕಿತ್ಸಾ ಮಾರ್ಗಗಳು",
      pathwaysSub: "ಬೆಳೆಯ ಹಂತ ಮತ್ತು ಪ್ರಮಾಣೀಕರಣ ಗುರಿಗಳ ಆಧಾರದ ಮೇಲೆ ನಿಮ್ಮ ಆದ್ಯತೆಯ ನಿರ್ವಹಣಾ ತಂತ್ರವನ್ನು ಆಯ್ಕೆಮಾಡಿ.",
      organicTab: "ಸಾವಯವ ಮತ್ತು ಪರಿಸರಸ್ನೇಹಿ",
      chemicalTab: "ರಾಸಾಯನಿಕ ಮತ್ತು ಉದ್ದೇಶಿತ",
      vetOrganicTab: "ಪೋಷಕ ಮತ್ತು ಗಿಡಮೂಲಿಕೆ ಆರೈಕೆ",
      vetChemicalTab: "ಪಶು ವೈದ್ಯಕೀಯ ಚಿಕಿತ್ಸಾ ಶಿಷ್ಟಾಚಾರ",
      biologicalProtocol: "ಜೈವಿಕ ನಿಯಂತ್ರಣ ಶಿಷ್ಟಾಚಾರ",
      chemicalProtocol: "ವ್ಯವಸ್ಥಿತ / ಸಂಪರ್ಕ ರಾಸಾಯನಿಕ ಸೂತ್ರ",
      vetHerbalProtocol: "ಗಿಡಮೂಲಿಕೆ ಮತ್ತು ಜೈವಿಕ ಸುರಕ್ಷತೆ",
      vetMedicalProtocol: "ಪಶು ವೈದ್ಯಕೀಯ ತಜ್ಞರ ಶಿಷ್ಟಾಚಾರ",
      prepMethod: "ತಯಾರಿ ಮತ್ತು ದುರ್ಬಲಗೊಳಿಸುವ ವಿಧಾನ",
      scheduleInterval: "ಸಿಂಪಡಣೆಯ ಆವರ್ತನ ಮತ್ತು ಮಧ್ಯಂತರ",
      culturalPractices: "ನೈರ್ಮಲ್ಯ ಮತ್ತು ಮುನ್ನೆಚ್ಚರಿಕೆ ಕ್ರಮಗಳು",
      activeMolecule: "ಸಕ್ರಿಯ ಅಣು / ಸೂತ್ರ",
      applicationRate: "ಸಿಂಪಡಣೆಯ ಪ್ರಮಾಣ",
      phiDays: "ಕೊಯ್ಲಿನ ಮುಂಚಿನ ಕಾಯುವಿಕೆ ಅವಧಿ (PHI)",
      mandatoryPhi: "ದಿನಗಳ ಕಡ್ಡಾಯ ತಡೆಹಿಡಿಯುವಿಕೆ",
      safetyPrecautions: "ರೈತರ ಮತ್ತು ಪರಿಸರ ಸುರಕ್ಷತಾ ಮುನ್ನೆಚ್ಚರಿಕೆಗಳು",
      locateMap: "ನಕ್ಷೆಯಲ್ಲಿ ಪತ್ತೆ ಮಾಡಿ",
      scanAnother: "ಇನ್ನೊಂದು ಸ್ಕ್ಯಾನ್ ಮಾಡಿ",
      listenAloud: "ಧ್ವನಿಯಲ್ಲಿ ಆಲಿಸಿ",
      stopSpeech: "ಧ್ವನಿ ನಿಲ್ಲಿಸಿ",
      copyRx: "ಚಿಕಿತ್ಸಾ ಚೀಟಿ ನಕಲಿಸಿ",
      copied: "ನಕಲಿಸಲಾಗಿದೆ!",
      cnnBadge: "ಡೀಪ್ CNN ವೈಶಿಷ್ಟ್ಯಗಳು"
    },
    map: {
      title: "ಪ್ರಾದೇಶಿಕ ರೋಗ ಹರಡುವಿಕೆ ನಕ್ಷೆ (GIS)",
      postGisBadge: "PostGIS ವೆಕ್ಟರ್ ಎಂಜಿನ್",
      subtitle: "ನೈಜ-ಸಮಯದ ಬೆಳೆ ರೋಗ ಹರಡುವಿಕೆ ಮತ್ತು ಸಾಂಕ್ರಾಮಿಕ ಅಪಾಯದ ನಕ್ಷೆ.",
      allCrops: "ಎಲ್ಲಾ ಬೆಳೆಗಳು",
      allSeverities: "ಎಲ್ಲಾ ತೀವ್ರತೆಗಳು",
      severeOnly: "ತೀವ್ರ ಮಾತ್ರ",
      moderate: "ಮಧ್ಯಮ",
      lowHealthy: "ಕಡಿಮೆ / ಆರೋಗ್ಯಕರ",
      myLocation: "ನನ್ನ ಸ್ಥಳ",
      severeHotspots: "ತೀವ್ರ ರೋಗಪೀಡಿತ ವಲಯಗಳು",
      totalClusters: "ಒಟ್ಟು ಪತ್ತೆಯಾದ ಕ್ಲಸ್ಟರ್‌ಗಳು",
      activeList: "ಸಕ್ರಿಯ ರೋಗ ಹರಡುವಿಕೆ ಪಟ್ಟಿ",
      liveFeed: "ಲೈವ್ ಫೀಡ್",
      distanceAway: "ಕಿ.ಮೀ ದೂರದಲ್ಲಿದೆ",
      certainty: "ನಿಖರತೆ"
    },
    history: {
      title: "ರೈತರ ರೋಗನಿರ್ಣಯ ಲಾಗ್ ಮತ್ತು ಇತಿಹಾಸ",
      totalRecords: "ಒಟ್ಟು ದಾಖಲೆಗಳು",
      subtitle: "ಕ್ಷೇತ್ರ ಸ್ಕ್ಯಾನ್‌ಗಳು, ಪತ್ತೆಯಾದ ರೋಗಕಾರಕಗಳು ಮತ್ತು ಶಿಫಾರಸು ಮಾಡಿದ ಚಿಕಿತ್ಸೆಗಳ ದಾಖಲೆ.",
      searchPlaceholder: "ಬೆಳೆ ಅಥವಾ ರೋಗ ಹುಡುಕಿ...",
      exportLog: "ಲಾಗ್ ಡೌನ್‌ಲೋಡ್",
      noScansTitle: "ಯಾವುದೇ ಸ್ಕ್ಯಾನ್ ಕಂಡುಬಂದಿಲ್ಲ",
      noScansDesc: "ರೋಗ ಸ್ಕ್ಯಾನ್ ಮಾಡಲು ಕ್ಯಾಮೆರಾ ಬಳಸಿ ಅಥವಾ ಮಾದರಿ ಗ್ಯಾಲರಿಯಿಂದ ಆಯ್ಕೆಮಾಡಿ.",
      organicRx: "ಸಾವಯವ ನಿಯಂತ್ರಣ ಪರಿಹಾರ",
      chemicalProtocol: "ರಾಸಾಯನಿಕ ನಿಯಂತ್ರಣ ಶಿಷ್ಟಾಚಾರ"
    },
    analytics: {
      title: "ಜಾಗತಿಕ ಕೃಷಿ ವಿಜ್ಞಾನ ಮತ್ತು ರೋಗ ಗುಪ್ತಚರ",
      badge: "ಒಟ್ಟು ಮೆಟ್ರಿಕ್‌ಗಳು",
      subtitle: "ಸಾಂಕ್ರಾಮಿಕ ರೋಗಶಾಸ್ತ್ರೀಯ ವಿತರಣೆ ಮತ್ತು ಬೆಳೆ ರೋಗ ಸಂವೇದನಾ ಸೂಚ್ಯಂಕ.",
      totalScans: "ಒಟ್ಟು ಕ್ಷೇತ್ರ ಸ್ಕ್ಯಾನ್‌ಗಳು",
      severeRisk: "ತೀವ್ರ ರೋಗ ಅಪಾಯ",
      sla: "ರೋಗನಿರ್ಣಯದ ವೇಗ (SLA)",
      cropsMonitored: "ಮೇಲ್ವಿಚಾರಣೆಯಲ್ಲಿರುವ ಬೆಳೆಗಳು",
      topCropsTitle: "ಹೆಚ್ಚು ವಿಶ್ಲೇಷಿಸಲ್ಪಟ್ಟ ಬೆಳೆಗಳು ಮತ್ತು ಅಪಾಯ",
      pathogenDistribution: "ರೋಗಕಾರಕ ವರ್ಗೀಕರಣ ವಿತರಣೆ",
      fungal: "ಶಿಲೀಂಧ್ರ ರೋಗಕಾರಕಗಳು (ಬ್ಲೈಟ್, ತುಕ್ಕು, ಕೊಳೆರೋಗ)",
      bacterial: "ಬ್ಯಾಕ್ಟೀರಿಯಾ ರೋಗಕಾರಕಗಳು (ಎಲೆ ಕರಕಲು, ಕ್ಯಾಂಕರ್)",
      viral: "ವೈರಲ್ ಸೋಂಕುಗಳು (ಎಲೆ ಸುರುಟು, ಮೊಸಾಯಿಕ್)",
      pests: "ಕೀಟ / ಪರಾವಲಂಬಿ ಬಾಧೆ (ಕಾಂಡ ಕೊರೆಯುವ ಹುಳು)",
      realtimeCloud: "ನೈಜ-ಸಮಯದ ಕ್ಲೌಡ್ ವಿಶ್ಲೇಷಣೆ",
      analyzedAcreage: "ವಿಶ್ಲೇಷಿತ ಕ್ಷೇತ್ರದ ಶೇಕಡಾವಾರು",
      subsecondEdge: "ಅತಿವೇಗದ ಎಡ್ಜ್ ವಿಶ್ಲೇಷಣೆ",
      stapleGrains: "ಮುಖ್ಯ ಧಾನ್ಯಗಳು, ತೋಟಗಾರಿಕೆ ಬೆಳೆಗಳು",
      frequency: "ಆವರ್ತನ",
      globalRatio: "ಜಾಗತಿಕ ಅನುಪಾತ",
      scansCount: "ಸ್ಕ್ಯಾನ್‌ಗಳು"
    },
    footer: {
      tagline: "ಸಾರ್ವತ್ರಿಕ ಬೆಳೆ ರೋಗಶಾಸ್ತ್ರ ಮತ್ತು ಕೃಷಿ ವಿಜ್ಞಾನ ಎಂಜಿನ್",
      fastapi: "ಫಾಸ್ಟ್-ಎಪಿಐ ಕೋರ್",
      groq: "ಗ್ರೋಕ್ LLaMA-3.2-11B ವಿಷನ್",
      postgis: "ಸುಪಬೇಸ್ PostGIS ರೆಡಿ"
    }
  },

  // 2. ENGLISH
  en: {
    brand: {
      title: "AgriVision AI",
      tagline: "Universal Crop Disease Diagnostic & Agronomy Engine",
      subtitle: "Next-generation agricultural diagnostics powered by Deep-CNN & Multi-Modal Vision",
      universalCore: "Universal Core",
      online: "Core Online",
      connecting: "Connecting",
      coreActive: "Core Active",
      deepCnnActive: "Deep CNN Active"
    },
    nav: {
      scan: "Scan & Diagnose",
      map: "Outbreak Map (GIS)",
      history: "Field Logs",
      analytics: "Analytics"
    },
    scanner: {
      targetCrop: "Target Crop / Livestock",
      autoDetect: "Auto-Detect (Crops & Livestock)",
      gpsCoordinates: "Field GPS Coordinates",
      gpsAcquired: "GPS Acquired",
      awaitingGps: "Awaiting Satellite Lock...",
      multiModalCore: "Multi-Modal + Deep CNN Core",
      multiModalSub: "PyTorch CNN + Agronomy Synthesizer",
      readyTitle: "Ready for Pathology Scan",
      readyDesc: "Position camera over the affected plant leaf or animal symptom, upload a photo, or choose a test sample.",
      openCamera: "Open Camera",
      uploadImage: "Upload Image",
      retake: "Retake",
      changeImage: "Change Image",
      runDiagnostic: "Run Diagnostic Engine",
      telemetryTitle: "Scanning tissue contours...",
      telemetrySla: "Universal Vision Pipeline • Latency < 200ms",
      telemetry: [
        "Acquiring high-resolution pixels...",
        "Running PyTorch Deep-CNN spatial convolution...",
        "Segmenting foliar contours & chlorophyll degradation...",
        "Scanning necrotic lesion boundaries & spore textures...",
        "Synthesizing biological & chemical dosage regimens..."
      ],
      galleryTitle: "Instant 1-Click Verification Gallery",
      gallerySub: "Select sample to test AI model instantly",
      plantBadge: "Plant",
      animalBadge: "Animal"
    },
    diagnostic: {
      veterinaryAlertTitle: "Veterinary Health Advisory",
      veterinaryWarningDesc: "This has been identified as an Animal / Livestock condition. NEVER apply agricultural crop pesticides or plant chemicals to animals. Consult a registered veterinarian.",
      invalidImageTitle: "No Agricultural Subject Detected",
      invalidImageDesc: "The uploaded image does not appear to contain a crop plant leaf or animal symptom. Please capture a clear, focused photo.",
      wrongPhotoTitle: "Error: Not a Plant Disease Photo",
      wrongPhotoDesc: "The uploaded image is not a crop plant disease leaf (detected human, animal, vehicle, object, or non-botanical subject). AgriVision is strictly a crop plant pathology engine. Please upload a clear photo of an affected plant leaf showing disease symptoms.",
      wrongPhotoBadge: "ERROR: NOT A PLANT LEAF",
      retakeCorrectLeaf: "Upload Plant Disease Leaf Photo",
      cnnDomainClassification: "CNN Domain Classification",
      certainty: "Model Certainty",
      severityTitle: "Infection Severity",
      surfaceArea: "lesion surface area",
      observedSymptoms: "Observed Symptoms",
      morphologyValidated: "Foliar morphology validated",
      vetValidated: "Veterinary morphology validated",
      pathwaysTitle: "Actionable Agronomy Treatment Pathways",
      pathwaysSub: "Select your preferred management strategy based on crop lifecycle and certification goals.",
      organicTab: "Organic & Eco-Friendly",
      chemicalTab: "Chemical & Targeted",
      vetOrganicTab: "Supportive & Herbal Care",
      vetChemicalTab: "Veterinary Medical Protocol",
      biologicalProtocol: "Biological Control Protocol",
      chemicalProtocol: "Systemic / Contact Molecule",
      vetHerbalProtocol: "Herbal & Biosecurity Protocol",
      vetMedicalProtocol: "Veterinary Medical Strategy",
      prepMethod: "Preparation & Dilution Method",
      scheduleInterval: "Spray Frequency & Interval",
      culturalPractices: "Cultural & Preventive Hygiene Practices",
      activeMolecule: "Active Formulation",
      applicationRate: "Application Rate",
      phiDays: "Pre-Harvest Interval (PHI)",
      mandatoryPhi: "Days Mandatory Withholding",
      safetyPrecautions: "Mandatory Safety & Environmental Precautions",
      locateMap: "Locate On Outbreak Map",
      scanAnother: "Scan Another Image",
      listenAloud: "Listen Aloud",
      stopSpeech: "Stop Speech",
      copyRx: "Copy Rx",
      copied: "Copied!",
      cnnBadge: "Deep-CNN Features"
    },
    map: {
      title: "Spatial Outbreak GIS Tracker",
      postGisBadge: "PostGIS Vector Engine",
      subtitle: "Real-time geospatial epidemiological mapping of crop disease clusters and contagion risks.",
      allCrops: "All Crops",
      allSeverities: "All Severities",
      severeOnly: "Severe Only",
      moderate: "Moderate",
      lowHealthy: "Low / Healthy",
      myLocation: "My Location",
      severeHotspots: "Severe Hotspots",
      totalClusters: "Total Clusters Mapped",
      activeList: "Active Outbreak List",
      liveFeed: "Live Feed",
      distanceAway: "km away",
      certainty: "Certainty"
    },
    history: {
      title: "Farmer Diagnostic Log & History",
      totalRecords: "Total Records",
      subtitle: "Historical trace of field scans, identified pathogens, and prescribed agronomy treatments.",
      searchPlaceholder: "Search crop or disease...",
      exportLog: "Export Log",
      noScansTitle: "No field scans found",
      noScansDesc: "Scan a crop leaf or use the 1-click test gallery to record disease scans to this ledger.",
      organicRx: "Organic Control Prescription",
      chemicalProtocol: "Chemical Control Protocol"
    },
    analytics: {
      title: "Global Agronomy & Pathology Intelligence",
      badge: "Aggregated Metrics",
      subtitle: "Epidemiological distribution, crop pathogen vulnerability index, and field diagnostic throughput.",
      totalScans: "Total Field Scans",
      severeRisk: "Severe Outbreak Risk",
      sla: "Diagnostic SLA",
      cropsMonitored: "Crop Families Monitored",
      topCropsTitle: "Most Analyzed Crops & Vulnerability",
      pathogenDistribution: "Pathogen Classification Distribution",
      fungal: "Fungal Pathogens (Blight, Rust, Koleroga)",
      bacterial: "Bacterial Pathogens (Leaf Blight, Canker)",
      viral: "Viral Infections (Leaf Curl, Mosaic)",
      pests: "Pest Infestation (Stem Borers, Armyworm)",
      realtimeCloud: "Real-time cloud inference",
      analyzedAcreage: "of analyzed acreage",
      subsecondEdge: "Sub-second edge inference",
      stapleGrains: "Staple grains, horticulture, cash",
      frequency: "Frequency",
      globalRatio: "Global Ratio",
      scansCount: "scans"
    },
    footer: {
      tagline: "Universal Crop Pathology & Agronomy Engine",
      fastapi: "FastAPI Core",
      groq: "Groq LLaMA-3.2-11B Vision",
      postgis: "Supabase PostGIS Ready"
    }
  },

  // 3. HINDI (हिंदी)
  hi: {
    brand: {
      title: "एग्रीविज़न AI",
      tagline: "सार्वभौमिक फसल रोग निदान और कृषि विज्ञान इंजन",
      subtitle: "डीप-सीएनएन और मल्टी-मोडल विज़न द्वारा संचालित स्मार्ट कृषि निदान",
      universalCore: "सार्वभौमिक कोर",
      online: "कोर सक्रिय",
      connecting: "कनेक्ट हो रहा है",
      coreActive: "कोर चालू है",
      deepCnnActive: "डीप CNN सक्रिय"
    },
    nav: {
      scan: "स्कैन और निदान",
      map: "प्रकोप मानचित्र (GIS)",
      history: "फील्ड लॉग्स",
      analytics: "विश्लेषण"
    },
    scanner: {
      targetCrop: "लक्षित फसल / पशु",
      autoDetect: "ऑटो-डिटेक्ट (फसल और पशु)",
      gpsCoordinates: "खेत जीपीएस निर्देशांक",
      gpsAcquired: "जीपीएस प्राप्त हुआ",
      awaitingGps: "सैटेलाइट सिग्नल की प्रतीक्षा...",
      multiModalCore: "मल्टी-मॉडल + डीप CNN कोर",
      multiModalSub: "PyTorch CNN + कृषि संश्लेषण",
      readyTitle: "फसल रोग निदान के लिए तैयार",
      readyDesc: "प्रभावित पत्ती या पशु के लक्षण पर कैमरा रखें, फोटो अपलोड करें या नमूना चुनें।",
      openCamera: "कैमरा खोलें",
      uploadImage: "फोटो अपलोड करें",
      retake: "पुनः लें",
      changeImage: "फोटो बदलें",
      runDiagnostic: "निदान इंजन चलाएं",
      telemetryTitle: "पत्ती के ऊतक का विश्लेषण...",
      telemetrySla: "विज़न पाइपलाइन • प्रतिक्रिया समय < 200ms",
      telemetry: [
        "उच्च-रिज़ॉल्यूशन पिक्सेल प्राप्त किए जा रहे हैं...",
        "PyTorch डीप-CNN कनवल्शन प्रसंस्करण जारी है...",
        "पत्ती के क्लोरोफिल क्षरण का विश्लेषण...",
        "रोग के धब्बों और फफूंद बनावट की स्कैनिंग...",
        "जैविक और रासायनिक खुराक तैयार की जा रही है..."
      ],
      galleryTitle: "त्वरित 1-क्लिक परीक्षण गैलरी",
      gallerySub: "मॉडल का त्वरित परीक्षण करने के लिए नमूना चुनें",
      plantBadge: "पौधा",
      animalBadge: "पशु"
    },
    diagnostic: {
      veterinaryAlertTitle: "पशु चिकित्सा आपातकालीन सलाह",
      veterinaryWarningDesc: "यह एक पशु/मवेशी रोग है। फसलों वाली कीटनाशक दवा पशुओं पर कभी न लगाएं। तुरंत पशु चिकित्सक से संपर्क करें।",
      invalidImageTitle: "कोई कृषि विषय नहीं मिला",
      invalidImageDesc: "अपलोड की गई फोटो में फसल या पशु रोग के लक्षण नहीं मिले हैं। कृपया स्पष्ट फोटो लें।",
      wrongPhotoTitle: "त्रुटि: यह किसी पौधे की बीमारी का फोटो नहीं है",
      wrongPhotoDesc: "अपलोड किया गया फोटो किसी पौधे या फसल की पत्ती का नहीं है (मानव, पशु, वस्तु या अन्य गैर-कृषि विषय)। एग्रीविज़न केवल फसलों के पत्तों की बीमारी जांचने के लिए है। कृपया प्रभावित पौधे की पत्ती का स्पष्ट फोटो अपलोड करें।",
      wrongPhotoBadge: "त्रुटि: गलत फोटो (पौधे की पत्ती नहीं)",
      retakeCorrectLeaf: "पौधे की पत्ती का फोटो अपलोड करें",
      cnnDomainClassification: "CNN डोमेन वर्गीकरण",
      certainty: "मॉडल सटीकता",
      severityTitle: "संक्रमण गंभीरता",
      surfaceArea: "प्रभावित पत्ती क्षेत्र",
      observedSymptoms: "देखे गए लक्षण",
      morphologyValidated: "पत्ती संरचना सत्यापित",
      vetValidated: "पशु रोग सत्यापित",
      pathwaysTitle: "व्यावहारिक कृषि उपचार मार्ग",
      pathwaysSub: "फसल चक्र और आवश्यकताओं के अनुसार अपना पसंदीदा उपचार चुनें।",
      organicTab: "जैविक और पर्यावरण-अनुकूल",
      chemicalTab: "रासायनिक और लक्षित",
      vetOrganicTab: "सहायक और हर्बल देखभाल",
      vetChemicalTab: "पशु चिकित्सा प्रोटोकॉल",
      biologicalProtocol: "जैविक नियंत्रण प्रोटोकॉल",
      chemicalProtocol: "प्रणालीगत रासायनिक अणु",
      vetHerbalProtocol: "हर्बल और जैव-सुरक्षा उपाय",
      vetMedicalProtocol: "पशु चिकित्सा रणनीति",
      prepMethod: "तैयारी और घोल बनाने की विधि",
      scheduleInterval: "छिड़काव का अंतराल",
      culturalPractices: "रोकथाम और स्वच्छता उपाय",
      activeMolecule: "सक्रिय घटक",
      applicationRate: "छिड़काव दर",
      phiDays: "कटाई पूर्व प्रतीक्षा अवधि (PHI)",
      mandatoryPhi: "दिनों का अनिवार्य प्रतिबंध",
      safetyPrecautions: "अनिवार्य सुरक्षा व पर्यावरण सावधानियां",
      locateMap: "मानचित्र पर खोजें",
      scanAnother: "अन्य स्कैन करें",
      listenAloud: "आवाज़ में सुनें",
      stopSpeech: "आवाज़ बंद करें",
      copyRx: "नुस्खा कॉपी करें",
      copied: "कॉपी हो गया!",
      cnnBadge: "डीप-CNN मेट्रिक्स"
    },
    map: {
      title: "स्थानिक प्रकोप जीआईएस ट्रैकर",
      postGisBadge: "PostGIS वेक्टर इंजन",
      subtitle: "फसल रोग प्रकोप और संक्रमण जोखिम का वास्तविक समय का नक्शा।",
      allCrops: "सभी फसलें",
      allSeverities: "सभी गंभीरता स्तर",
      severeOnly: "केवल गंभीर",
      moderate: "मध्यम",
      lowHealthy: "कम / स्वस्थ",
      myLocation: "मेरा स्थान",
      severeHotspots: "गंभीर प्रकोप क्षेत्र",
      totalClusters: "कुल चिह्नित प्रकोप",
      activeList: "सक्रिय प्रकोप सूची",
      liveFeed: "लाइव फीड",
      distanceAway: "किमी दूर",
      certainty: "निश्चितता"
    },
    history: {
      title: "किसान नैदानिक रिकॉर्ड और इतिहास",
      totalRecords: "कुल रिकॉर्ड",
      subtitle: "खेत स्कैन और निर्धारित उपचारों का ऐतिहासिक रिकॉर्ड।",
      searchPlaceholder: "फसल या रोग खोजें...",
      exportLog: "लॉग डाउनलोड करें",
      noScansTitle: "कोई स्कैन नहीं मिला",
      noScansDesc: "रोग स्कैन करने के लिए कैमरा खोलें या नमूना गैलरी से चुनें।",
      organicRx: "जैविक नियंत्रण नुस्खा",
      chemicalProtocol: "रासायनिक नियंत्रण प्रोटोकॉल"
    },
    analytics: {
      title: "वैश्विक कृषि विज्ञान और रोग विश्लेषण",
      badge: "कुल आंकड़े",
      subtitle: "महामारी विज्ञान वितरण और फसल रोग संवेदनशीलता सूचकांक।",
      totalScans: "कुल फील्ड स्कैन",
      severeRisk: "गंभीर प्रकोप जोखिम",
      sla: "निदान गति (SLA)",
      cropsMonitored: "निगरानी की जा रही फसलें",
      topCropsTitle: "सर्वाधिक विश्लेषित फसलें",
      pathogenDistribution: "रोगज़नक़ वर्गीकरण वितरण",
      fungal: "कवक रोगज़नक़ (झुलसा, रतुआ, सड़न)",
      bacterial: "जीवाणु रोगज़नक़ (पत्ती झुलसा, कैंकर)",
      viral: "विषाणु संक्रमण (पत्ती मरोड़, मोज़ेक)",
      pests: "कीट प्रकोप (तना छेदक, इल्ली)",
      realtimeCloud: "वास्तविक समय क्लाउड निष्कर्ष",
      analyzedAcreage: "विश्लेषित क्षेत्र का प्रतिशत",
      subsecondEdge: "अल्ट्रा-फास्ट एज निष्कर्ष",
      stapleGrains: "अनाज, बागवानी और नकदी फसलें",
      frequency: "आवृत्ति",
      globalRatio: "वैश्विक अनुपात",
      scansCount: "स्कैन"
    },
    footer: {
      tagline: "सार्वभौमिक फसल रोगविज्ञान और कृषि विज्ञान इंजन",
      fastapi: "फास्ट-एपीआई कोर",
      groq: "ग्रोक LLaMA-3.2-11B विज़न",
      postgis: "सुपाबेस PostGIS तैयार"
    }
  },

  // 4. SPANISH
  es: {
    brand: {
      title: "AgriVision AI",
      tagline: "Motor Universal de Diagnóstico y Agronomía de Cultivos",
      subtitle: "Diagnóstico agrícola impulsado por Deep-CNN y Visión Multimodal",
      universalCore: "Núcleo Universal",
      online: "En Línea",
      connecting: "Conectando",
      coreActive: "Núcleo Activo",
      deepCnnActive: "Deep CNN Activo"
    },
    nav: {
      scan: "Escanear y Diagnosticar",
      map: "Mapa de Brotes (GIS)",
      history: "Registros de Campo",
      analytics: "Analítica"
    },
    scanner: {
      targetCrop: "Cultivo / Ganado Objetivo",
      autoDetect: "Detección Automática (Cultivos y Ganado)",
      gpsCoordinates: "Coordenadas GPS del Campo",
      gpsAcquired: "GPS Adquirido",
      awaitingGps: "Esperando señal satelital...",
      multiModalCore: "Núcleo Multimodal + Deep CNN",
      multiModalSub: "PyTorch CNN + Síntesis Agronómica",
      readyTitle: "Listo para Escaneo de Patología",
      readyDesc: "Coloque la cámara sobre la hoja o síntoma animal, cargue una foto o elija una muestra.",
      openCamera: "Abrir Cámara",
      uploadImage: "Cargar Imagen",
      retake: "Volver a Tomar",
      changeImage: "Cambiar Imagen",
      runDiagnostic: "Ejecutar Diagnóstico",
      telemetryTitle: "Escaneando tejido foliar...",
      telemetrySla: "Pipeline de Visión • Latencia < 200ms",
      telemetry: [
        "Adquiriendo píxeles de alta resolución...",
        "Ejecutando convolución espacial PyTorch Deep-CNN...",
        "Segmentando contornos foliares y degradación de clorofila...",
        "Escaneando bordes de lesiones necróticas...",
        "Sintetizando dosis biológicas y químicas..."
      ],
      galleryTitle: "Galería de Verificación en 1 Clic",
      gallerySub: "Seleccione una muestra para probar el modelo",
      plantBadge: "Planta",
      animalBadge: "Animal"
    },
    diagnostic: {
      veterinaryAlertTitle: "Aviso Veterinario de Emergencia",
      veterinaryWarningDesc: "Esta es una condición animal/ganadera. NUNCA aplique pesticidas agrícolas a animales. Consulte a un veterinario.",
      invalidImageTitle: "Sujeto no Agrícola Detectado",
      invalidImageDesc: "La imagen no parece contener hojas ni síntomas animales. Por favor capture una foto clara.",
      wrongPhotoTitle: "Error: No es una foto de enfermedad de planta",
      wrongPhotoDesc: "La imagen cargada no es una hoja de cultivo (se detectó un humano, animal, vehículo u objeto no botánico). AgriVision es un motor exclusivo para hojas de plantas. Cargue una foto clara de una hoja enferma.",
      wrongPhotoBadge: "ERROR: NO ES HOJA DE CULTIVO",
      retakeCorrectLeaf: "Subir foto de hoja de cultivo",
      cnnDomainClassification: "Clasificación de Dominio CNN",
      certainty: "Certeza del Modelo",
      severityTitle: "Severidad de Infección",
      surfaceArea: "área de lesión foliar",
      observedSymptoms: "Síntomas Observados",
      morphologyValidated: "Morfología foliar validada",
      vetValidated: "Patología veterinaria validada",
      pathwaysTitle: "Vías de Tratamiento Agronómico",
      pathwaysSub: "Seleccione su estrategia de manejo según las necesidades del cultivo.",
      organicTab: "Orgánico y Ecológico",
      chemicalTab: "Químico y Dirigido",
      vetOrganicTab: "Cuidado de Apoyo y Herbal",
      vetChemicalTab: "Protocolo Médico Veterinario",
      biologicalProtocol: "Protocolo de Control Biológico",
      chemicalProtocol: "Molécula Química Sistémica",
      vetHerbalProtocol: "Protocolo de Bioseguridad y Herbal",
      vetMedicalProtocol: "Estrategia Médica Veterinaria",
      prepMethod: "Método de Preparación y Dilución",
      scheduleInterval: "Frecuencia e Intervalo de Pulverización",
      culturalPractices: "Prácticas de Higiene y Prevención",
      activeMolecule: "Formulación Activa",
      applicationRate: "Dosis de Aplicación",
      phiDays: "Intervalo Pre-Cosecha (PHI)",
      mandatoryPhi: "Días de Retiro Obligatorio",
      safetyPrecautions: "Precauciones de Seguridad y Ambientales",
      locateMap: "Ubicar en el Mapa",
      scanAnother: "Escanear Otra Imagen",
      listenAloud: "Escuchar en Audio",
      stopSpeech: "Detener Audio",
      copyRx: "Copiar Receta",
      copied: "¡Copiado!",
      cnnBadge: "Métricas Deep-CNN"
    },
    map: {
      title: "Rastreador Espacial de Brotes GIS",
      postGisBadge: "Motor Vectorial PostGIS",
      subtitle: "Mapeo epidemiológico en tiempo real de brotes y riesgos de contagio.",
      allCrops: "Todos los Cultivos",
      allSeverities: "Todas las Severidades",
      severeOnly: "Solo Severo",
      moderate: "Moderado",
      lowHealthy: "Bajo / Sano",
      myLocation: "Mi Ubicación",
      severeHotspots: "Focos Severos",
      totalClusters: "Total de Brotes Mapeados",
      activeList: "Lista de Brotes Activos",
      liveFeed: "En Vivo",
      distanceAway: "km de distancia",
      certainty: "Certeza"
    },
    history: {
      title: "Registro de Campo e Historial",
      totalRecords: "Registros Totales",
      subtitle: "Historial de escaneos de campo y tratamientos prescritos.",
      searchPlaceholder: "Buscar cultivo o enfermedad...",
      exportLog: "Exportar Registro",
      noScansTitle: "Sin escaneos registrados",
      noScansDesc: "Escanee una hoja o use la galería para registrar datos.",
      organicRx: "Receta de Control Orgánico",
      chemicalProtocol: "Protocolo de Control Químico"
    },
    analytics: {
      title: "Inteligencia Agronómica y Patológica Global",
      badge: "Métricas Agregadas",
      subtitle: "Distribución epidemiológica e índice de vulnerabilidad.",
      totalScans: "Total de Escaneos",
      severeRisk: "Riesgo de Brote Severo",
      sla: "Velocidad de Diagnóstico (SLA)",
      cropsMonitored: "Familias Monitoreadas",
      topCropsTitle: "Cultivos Más Analizados",
      pathogenDistribution: "Distribución de Patógenos",
      fungal: "Patógenos Fúngicos (Tizón, Roya, Podredumbre)",
      bacterial: "Patógenos Bacterianos (Tizón Foliar, Cancro)",
      viral: "Infecciones Virales (Enrollamiento, Mosaico)",
      pests: "Infestación de Plagas (Barrenadores, Gusano)",
      realtimeCloud: "Inferencia en la nube en tiempo real",
      analyzedAcreage: "de superficie analizada",
      subsecondEdge: "Inferencia edge ultrarrápida",
      stapleGrains: "Granos básicos, horticultura, comerciales",
      frequency: "Frecuencia",
      globalRatio: "Proporción Global",
      scansCount: "escaneos"
    },
    footer: {
      tagline: "Motor Universal de Patología y Agronomía de Cultivos",
      fastapi: "Núcleo FastAPI",
      groq: "Groq LLaMA-3.2-11B Vision",
      postgis: "Supabase PostGIS Integrado"
    }
  },

  // 5. SWAHILI
  sw: {
    brand: {
      title: "AgriVision AI",
      tagline: "Injini ya Utambuzi wa Magonjwa ya Mimea na Kilimo",
      subtitle: "Uchunguzi wa kisasa wa kilimo unaoendeshwa na Deep-CNN",
      universalCore: "Kiini Kikuu",
      online: "Mtandaoni",
      connecting: "Inaunganisha",
      coreActive: "Kiini Kinafanya Kazi",
      deepCnnActive: "Deep CNN Inafanya Kazi"
    },
    nav: {
      scan: "Pima na Tambua",
      map: "Ramani ya Mlipuko (GIS)",
      history: "Kumbukumbu za Shamba",
      analytics: "Takwimu"
    },
    scanner: {
      targetCrop: "Zao / Mifugo Inayolengwa",
      autoDetect: "Gundua Moja kwa Moja (Mimea na Mifugo)",
      gpsCoordinates: "Vipimo vya GPS vya Shamba",
      gpsAcquired: "GPS Imepatikana",
      awaitingGps: "Inasubiri mawimbi ya satelaiti...",
      multiModalCore: "Kiini cha Multi-Modal + Deep CNN",
      multiModalSub: "PyTorch CNN + Usanisi wa Kilimo",
      readyTitle: "Tayari kwa Uchunguzi wa Ugonjwa",
      readyDesc: "Weka kamera juu ya jani au dalili ya mnyama, pakia picha au chagua sampuli.",
      openCamera: "Fungua Kamera",
      uploadImage: "Pakia Picha",
      retake: "Piga Tena",
      changeImage: "Badilisha Picha",
      runDiagnostic: "Anzisha Injini ya Utambuzi",
      telemetryTitle: "Inachambua jani...",
      telemetrySla: "Mfumo wa Maono • Kasi < 200ms",
      telemetry: [
        "Inapokea picha ya ubora wa juu...",
        "Inaendesha usindikaji wa PyTorch Deep-CNN...",
        "Inachambua kuharibika kwa kijani cha jani...",
        "Inachunguza madoa na maambukizi...",
        "Inatayarisha tiba za kibiolojia na kemikali..."
      ],
      galleryTitle: "Sampuli za Jaribio la Papo Hapo",
      gallerySub: "Chagua sampuli kujaribu mfumo mara moja",
      plantBadge: "Mmea",
      animalBadge: "Mnyama"
    },
    diagnostic: {
      veterinaryAlertTitle: "Tahadhari ya Afya ya Mifugo",
      veterinaryWarningDesc: "Huu ni ugonjwa wa wanyama/mifugo. USITUMIE dawa za kilimo za mimea kwa wanyama. Wasiliana na daktari wa mifugo mara moja.",
      invalidImageTitle: "Hakuna Picha ya Kilimo Iliyogunduliwa",
      invalidImageDesc: "Picha haina majani ya mmea au dalili ya mifugo. Tafadhali piga picha wazi.",
      wrongPhotoTitle: "Hitilafu: Si picha ya ugonjwa wa mmea",
      wrongPhotoDesc: "Picha iliyopakiwa si jani la mmea lililoathiriwa (binadamu, mnyama, gari au kitu kimegunduliwa). AgriVision inachunguza magonjwa ya majani ya mimea pekee.",
      wrongPhotoBadge: "HITILAFU: PICHA ISIYO SAHIHI",
      retakeCorrectLeaf: "Pakia picha ya jani la mmea",
      cnnDomainClassification: "Uainishaji wa Eneo wa CNN",
      certainty: "Uhakika wa Mfumo",
      severityTitle: "Kiwango cha Ugonjwa",
      surfaceArea: "eneo lililoathirika",
      observedSymptoms: "Dalili Zilizobainika",
      morphologyValidated: "Muundo wa jani umethibitishwa",
      vetValidated: "Ugonjwa wa mifugo umethibitishwa",
      pathwaysTitle: "Mbinu za Matibabu ya Kilimo",
      pathwaysSub: "Chagua mbinu unayopendelea kulingana na mahitaji ya shamba.",
      organicTab: "Kibiolojia na Mazingira",
      chemicalTab: "Kemikali Maalum",
      vetOrganicTab: "Huduma Asilia ya Wanyama",
      vetChemicalTab: "Matibabu ya Daktari wa Mifugo",
      biologicalProtocol: "Mbinu za Asili za Kudhibiti",
      chemicalProtocol: "Dawa ya Kemikali",
      vetHerbalProtocol: "Mbinu za Kienyeji na Usafi",
      vetMedicalProtocol: "Ushauri wa Daktari wa Mifugo",
      prepMethod: "Njia ya Kutayarisha na Kuchanganya",
      scheduleInterval: "Muda na Ratiba ya Kunyunyizia",
      culturalPractices: "Mbinu za Usafi na Kuzuia",
      activeMolecule: "Kiambato Kikuu",
      applicationRate: "Kipimo cha Kutumia",
      phiDays: "Muda Kabla ya Kuvuna (PHI)",
      mandatoryPhi: "Siku za Lazima Kusubiri",
      safetyPrecautions: "Tahadhari za Usalama na Mazingira",
      locateMap: "Tafuta Kwenye Ramani",
      scanAnother: "Pima Picha Nyingine",
      listenAloud: "Sikiliza kwa Sauti",
      stopSpeech: "Simamisha Sauti",
      copyRx: "Nakili Maagizo",
      copied: "Imenakiliwa!",
      cnnBadge: "Vipimo vya Deep-CNN"
    },
    map: {
      title: "Ramani ya Kufuatilia Mlipuko wa Magonjwa",
      postGisBadge: "Injini ya PostGIS",
      subtitle: "Ufuatiliaji wa wakati halisi wa maeneo yenye mlipuko wa magonjwa ya mazao.",
      allCrops: "Mazao Yote",
      allSeverities: "Viwango Vyote",
      severeOnly: "Kiwango cha Juu Pekee",
      moderate: "Kiwango cha Kati",
      lowHealthy: "Kiwango cha Chini / Nzuri",
      myLocation: "Mahali Nilipo",
      severeHotspots: "Maeneo Hatari",
      totalClusters: "Jumla ya Maeneo Yaliyotambuliwa",
      activeList: "Orodha ya Mlipuko wa Magonjwa",
      liveFeed: "Mubashara",
      distanceAway: "km kutoka hapa",
      certainty: "Uhakika"
    },
    history: {
      title: "Kumbukumbu na Historia ya Shamba",
      totalRecords: "Jumla ya Rekodi",
      subtitle: "Historia ya uchunguzi wa shamba na matibabu yaliyopendekezwa.",
      searchPlaceholder: "Tafuta zao au ugonjwa...",
      exportLog: "Pakua Kumbukumbu",
      noScansTitle: "Hakuna vipimo vilivyopatikana",
      noScansDesc: "Pima jani au chagua sampuli kuanza kurekodi.",
      organicRx: "Tiba ya Asili",
      chemicalProtocol: "Tiba ya Kemikali"
    },
    analytics: {
      title: "Takwimu za Utafiti wa Magonjwa ya Kilimo",
      badge: "Vipimo Vilivyokusanywa",
      subtitle: "Mchanganuo wa hatari za magonjwa na kasi ya uchunguzi.",
      totalScans: "Jumla ya Vipimo vya Shamba",
      severeRisk: "Hatari ya Mlipuko Mkali",
      sla: "Kasi ya Utambuzi (SLA)",
      cropsMonitored: "Aina za Mazao Yanayofuatiliwa",
      topCropsTitle: "Mazao Yaliyochunguzwa Zaidi",
      pathogenDistribution: "Mgawanyo wa Aina za Vijidudu",
      fungal: "Vijidudu vya Kuvu (Kinyausi, Kutu, Kuoza)",
      bacterial: "Vijidudu vya Bakteria (Kinyausi cha Majani)",
      viral: "Maambukizi ya Virusi (Kukunja Majani, Madoa)",
      pests: "Mashambulizi ya Wadudu (Viwavi, Vidukari)",
      realtimeCloud: "Uchambuzi wa wingu wa moja kwa moja",
      analyzedAcreage: "ya eneo lililopimwa",
      subsecondEdge: "Uchambuzi wa haraka sana",
      stapleGrains: "Nafaka, mboga na mazao ya biashara",
      frequency: "Marudio",
      globalRatio: "Uwiano wa Jumla",
      scansCount: "vipimo"
    },
    footer: {
      tagline: "Injini ya Patholojia ya Mazao na Kilimo cha Kimataifa",
      fastapi: "Kiini cha FastAPI",
      groq: "Groq LLaMA-3.2-11B Vision",
      postgis: "Tayari kwa Supabase PostGIS"
    }
  },

  // 6. FRENCH
  fr: {
    brand: {
      title: "AgriVision AI",
      tagline: "Moteur Universel de Diagnostic des Maladies des Cultures",
      subtitle: "Diagnostic agricole avancé alimenté par Deep-CNN et Vision Multimodale",
      universalCore: "Noyau Universel",
      online: "En Ligne",
      connecting: "Connexion",
      coreActive: "Noyau Actif",
      deepCnnActive: "Deep CNN Actif"
    },
    nav: {
      scan: "Scanner & Diagnostiquer",
      map: "Carte des Foyers (GIS)",
      history: "Journaux de Terrain",
      analytics: "Analytique"
    },
    scanner: {
      targetCrop: "Culture / Bétail Cible",
      autoDetect: "Détection Automatique (Cultures et Bétail)",
      gpsCoordinates: "Coordonnées GPS du Champ",
      gpsAcquired: "GPS Acquis",
      awaitingGps: "En attente du signal satellite...",
      multiModalCore: "Noyau Multimodal + Deep CNN",
      multiModalSub: "PyTorch CNN + Synthèse Agronomique",
      readyTitle: "Prêt pour l'Analyse Phytopathologique",
      readyDesc: "Placez la caméra sur la feuille ou le symptôme animal, téléchargez une photo ou choisissez un échantillon.",
      openCamera: "Ouvrir la Caméra",
      uploadImage: "Télécharger une Image",
      retake: "Reprendre",
      changeImage: "Changer d'Image",
      runDiagnostic: "Lancer le Diagnostic",
      telemetryTitle: "Analyse du tissu végétal...",
      telemetrySla: "Pipeline de Vision • Latence < 200ms",
      telemetry: [
        "Acquisition de pixels haute résolution...",
        "Exécution de convolution spatiale PyTorch Deep-CNN...",
        "Segmentation des contours foliaires et de la chlorophylle...",
        "Analyse des bordures de lésions nécrotiques...",
        "Synthèse des posologies biologiques et chimiques..."
      ],
      galleryTitle: "Galerie de Vérification en 1 Clic",
      gallerySub: "Sélectionnez un échantillon pour tester le modèle immédiatement",
      plantBadge: "Plante",
      animalBadge: "Animal"
    },
    diagnostic: {
      veterinaryAlertTitle: "Avis Vétérinaire d'Urgence",
      veterinaryWarningDesc: "Ceci a été identifié comme une maladie animale/d'élevage. N'appliquez JAMAIS de pesticides agricoles aux animaux. Consultez un vétérinaire.",
      invalidImageTitle: "Aucun Sujet Agricole Détecté",
      invalidImageDesc: "L'image ne semble pas contenir de feuille de culture ou de symptôme animal. Veuillez prendre une photo claire.",
      wrongPhotoTitle: "Erreur : Ceci n'est pas une feuille de plante",
      wrongPhotoDesc: "L'image téléchargée n'est pas une feuille de culture (humain, animal, véhicule ou objet non végétal). AgriVision est exclusivement destiné aux maladies des feuilles de plantes. Veuillez télécharger une photo nette d'une feuille malade.",
      wrongPhotoBadge: "ERREUR : MAUVAISE PHOTO (NON VÉGÉTAL)",
      retakeCorrectLeaf: "Télécharger une feuille de plante",
      cnnDomainClassification: "Classification de Domaine CNN",
      certainty: "Certitude du Modèle",
      severityTitle: "Sévérité de l'Infection",
      surfaceArea: "surface foliaire atteinte",
      observedSymptoms: "Symptômes Observés",
      morphologyValidated: "Morphologie foliaire validée",
      vetValidated: "Pathologie vétérinaire validée",
      pathwaysTitle: "Protocoles de Traitement Agronomique",
      pathwaysSub: "Choisissez votre stratégie de gestion selon vos objectifs culturaux.",
      organicTab: "Biologique & Écologique",
      chemicalTab: "Chimique & Ciblé",
      vetOrganicTab: "Soins de Soutien & Phytothérapie",
      vetChemicalTab: "Protocole Médical Vétérinaire",
      biologicalProtocol: "Protocole de Contrôle Biologique",
      chemicalProtocol: "Molécule Chimique Systémique",
      vetHerbalProtocol: "Protocole Vétérinaire Naturel",
      vetMedicalProtocol: "Stratégie Médicale Vétérinaire",
      prepMethod: "Méthode de Préparation et Dilution",
      scheduleInterval: "Fréquence et Intervalle de Pulvérisation",
      culturalPractices: "Pratiques d'Hygiène et de Prévention",
      activeMolecule: "Formulation Active",
      applicationRate: "Dose d'Application",
      phiDays: "Délai Avant Récolte (DAR)",
      mandatoryPhi: "Jours de Retrait Obligatoires",
      safetyPrecautions: "Précautions de Sécurité et Environnementales",
      locateMap: "Localiser sur la Carte",
      scanAnother: "Analyser une Autre Image",
      listenAloud: "Écouter l'Audio",
      stopSpeech: "Arrêter l'Audio",
      copyRx: "Copier l'Ordonnance",
      copied: "Copié !",
      cnnBadge: "Métriques Deep-CNN"
    },
    map: {
      title: "Suivi Géospatial des Foyers (GIS)",
      postGisBadge: "Moteur Vectoriel PostGIS",
      subtitle: "Cartographie épidémiologique en temps réel des foyers de maladies.",
      allCrops: "Toutes les Cultures",
      allSeverities: "Toutes les Sévérités",
      severeOnly: "Sévère Uniquement",
      moderate: "Modéré",
      lowHealthy: "Faible / Sain",
      myLocation: "Ma Position",
      severeHotspots: "Foyers Sévères",
      totalClusters: "Total des Foyers Répertoriés",
      activeList: "Liste des Foyers Actifs",
      liveFeed: "Flux en Direct",
      distanceAway: "km d'ici",
      certainty: "Certitude"
    },
    history: {
      title: "Journal et Historique de Terrain",
      totalRecords: "Total des Enregistrements",
      subtitle: "Historique des diagnostics de terrain et traitements prescrits.",
      searchPlaceholder: "Rechercher une culture ou maladie...",
      exportLog: "Exporter le Journal",
      noScansTitle: "Aucun scan trouvé",
      noScansDesc: "Scannez une feuille ou utilisez la galerie pour enregistrer des diagnostics.",
      organicRx: "Prescription Biologique",
      chemicalProtocol: "Protocole Chimique"
    },
    analytics: {
      title: "Intelligence Agronomique et Pathologique Mondiale",
      badge: "Données Agrégées",
      subtitle: "Distribution épidémiologique et vulnérabilité des cultures.",
      totalScans: "Total des Scans de Terrain",
      severeRisk: "Risque de Foyer Sévère",
      sla: "Rapidité du Diagnostic (SLA)",
      cropsMonitored: "Familles de Cultures Surveillées",
      topCropsTitle: "Cultures les Plus Analysées",
      pathogenDistribution: "Répartition des Classes de Pathogènes",
      fungal: "Pathogènes Fongiques (Mildiou, Rouille, Pourriture)",
      bacterial: "Pathogènes Bactériens (Flétrissement, Chancre)",
      viral: "Infections Virales (Enroulement, Mosaïque)",
      pests: "Infestations Parasitaires (Ravageurs, Chenilles)",
      realtimeCloud: "Inférence cloud en temps réel",
      analyzedAcreage: "de la superficie analysée",
      subsecondEdge: "Inférence edge ultra-rapide",
      stapleGrains: "Céréales, horticulture, cultures de rente",
      frequency: "Fréquence",
      globalRatio: "Ratio Global",
      scansCount: "analyses"
    },
    footer: {
      tagline: "Moteur Universel de Pathologie Végétale et d'Agronomie",
      fastapi: "Noyau FastAPI",
      groq: "Groq LLaMA-3.2-11B Vision",
      postgis: "Prêt pour Supabase PostGIS"
    }
  }
};
