<template>
  <ExamineRequestInfoExpandable class="text-sm" title="Applicant Information">
    <template #minimized>
      <ExamineRequestInfoApplicantMinimized />
    </template>

    <template #popup>
      <ExamineRequestInfoApplicantComplete />
    </template>

    <template #maximized>
      <ExamineRequestInfoApplicantComplete />
    </template>

    <template #editable>
      <ExamineRequestInfoApplicantEditable />
    </template>
  </ExamineRequestInfoExpandable>
</template>
