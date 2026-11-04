enum ConsentRequired {
  All = 'All',
  Yes = 'Yes',
  No = 'No',
  Received = 'Received',
  Waived = 'Waived'
}

enum Priority {
  All = 'All',
  Priority = 'Priority',
  Standard = 'Standard',
}

enum ClientNotification {
  All = 'All',
  Notified = 'Notified',
  NotNotified = 'Not Notified',
}

enum Submitted {
  All = 'All',
  Today = 'Today',
  Days7 = '7 days',
  Days30 = '30 days',
  Days90 = '90 days',
  Year1 = '1 year',
  Years3 = '3 years',
  Years5 = '5 years',
  Custom = 'Custom',
}

enum LastUpdate {
  All = 'All',
  Today = 'Today',
  Yesterday = 'Yesterday',
  Days2 = '2 days',
  Days7 = '7 days',
  Days30 = '30 days'
}

export {
  ConsentRequired,
  Priority,
  ClientNotification,
  Submitted,
  LastUpdate,
}
