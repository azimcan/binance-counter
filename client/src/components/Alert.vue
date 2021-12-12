<template>
  <div>
    <div class="alert alert-success alert-dismissible fade show" role="alert">
      {{ message }}
      <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    </div>
    <br>
  </div>
</template>

<script>
export default {
  props: ['message'],
};
</script>
